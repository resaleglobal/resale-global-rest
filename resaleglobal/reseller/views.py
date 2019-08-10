from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from resaleglobal.permissions import ResellerPermission
from resaleglobal.account.models import UserResellerAssignment, Reseller, Consignor, RCRelationship, UserConsignorAssignment

from .models import Category, Item, CategoryResellerRelationship, Department, Section, Attributes, CategoryAttributes, ItemAttributes

from django.db.models import Q
import json

from pprint import pprint
import datetime
import hashlib
import decimal
from django.conf import settings
import shopify

User = get_user_model()


class AttributesView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    category_id = kwargs['categoryId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    category = Category.objects.filter(pk=category_id).first()
    query_attributes = CategoryAttributes.objects.filter(category=category)

    attributes = []
    for attribute in query_attributes:
      attributes.append(attribute.json())

    return Response(attributes)


class ConsignorsView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    relationships = RCRelationship.objects.filter(reseller=reseller)
    categories = Category.objects.filter(Q(reseller=reseller) | Q(reseller=None))

    consignors = []
    for r in relationships:
      consignors.append(r.get_consignor())

    return Response(consignors)
    

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()

    account_name = request.data.get('accountName')
    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')
    if account_name is None:
      account_name = first_name + " " + last_name
    email = request.data.get('email')
    number = request.data.get('number')

    new_user = User.objects.create(
      email=email, can_login=False, is_registered=True, date_joined=datetime.datetime.now(datetime.timezone.utc), first_name=first_name, last_name=last_name, number=number
    )

    consignor = Consignor.objects.create(name=account_name, number=number, email=email)

    assignment = UserConsignorAssignment.objects.create(user=new_user, consignor=consignor, main_contact=True)

    RCRelationship.objects.create(consignor=consignor, reseller=reseller)

    token = hashlib.sha512(str(email + 'consignor' + reseller.domain + str(consignor.pk) + settings.INVITE_SALT).encode('utf-8')).hexdigest()

    url = "/invite-consignor?token=" + token + "&email=" + email + "&domain=" + reseller.domain + "&consignor=" + str(consignor.pk)

    return Response({
      'url': url
    })

class SectionsView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()

    department_id = request.GET.get('departmentId')

    if department_id is not None:
      department = Department.objects.filter(pk=department_id).first()
      selected_sections = Section.objects.filter(Q(reseller=reseller, department=department) | Q(reseller=None, department=department))
    else:
      selected_sections = Section.objects.filter(Q(reseller=reseller) | Q(reseller=None))

    sections = []
    for section in selected_sections:
      sections.append(section.json())

    return Response(sections)

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    department_id = request.data.get('departmentId')
    name = request.data.get('sectionName')
    reseller = Reseller.objects.filter(pk=account_id).first()
    department = Department.objects.filter(pk=department_id).first()
    
    Section(name=name, reseller=reseller, department=department).save()

    return Response(status=status.HTTP_201_CREATED)


class DepartmentsView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    selected_departments = Department.objects.filter(Q(reseller=reseller) | Q(reseller=None))

    departments = []
    for department in selected_departments:
      departments.append(department.json())

    return Response(departments)

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    name = request.data.get('departmentName')

    Department(name=name, reseller=reseller).save()

    return Response(status=status.HTTP_201_CREATED)


class CategoriesView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    categories = Category.objects.filter(Q(reseller=reseller) | Q(reseller=None)).order_by('section__department__name')
    selected_categories = list(CategoryResellerRelationship.objects.filter(reseller=reseller, category__in=categories).values_list('category__id', flat=True))

    cats = []
    for cat in categories:
      attributes = CategoryAttributes.objects.filter(category=cat)
      next_cat = cat.json()
      next_cat['attributes'] = [at.json() for at in attributes]
      next_cat['selected'] = next_cat['id'] in selected_categories
      cats.append(next_cat)

    return Response(cats)

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    name = request.data.get('category')
    section_id = request.data.get('sectionId')
    section = Section.objects.filter(pk=section_id).first()

    category = Category(name=name, section=section, reseller=reseller)
    category.save()

    selected = request.data.get('selected')

    if (selected):
      CategoryResellerRelationship(reseller=reseller, category=category).save()

    attributes = request.data.get('attributes')

    for a in attributes:
      attribute = Attributes.objects.filter(name=a).first()
      if attribute is None:
        attribute = Attributes(name=a)
        attribute.save()
      CategoryAttributes(reseller=reseller, category=category, attribute=attribute).save()

    return Response(status=status.HTTP_201_CREATED)

class SelectedCategoriesView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    selected_categories = CategoryResellerRelationship.objects.filter(reseller=reseller)
    cats = []
    for cat in selected_categories:
      cats.append(cat.json())

    return Response(cats)

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    category_ids = request.POST.getlist('categoryId')
    reseller = Reseller.objects.filter(pk=account_id).first()
    body = json.loads(request.body)
    for cat in body:
      Category(name=cat['name']).save()

    return Response(status=status.HTTP_201_CREATED)

class ItemsView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()

    search_items = Item.objects.filter(reseller=reseller).order_by("title")

    items = []

    for i in search_items:
      items.append(i.item_list())

    return Response(items)

  def post(self, request, *args, **kwargs):
    reseller_id = kwargs['accountId']

    dzero = decimal.Decimal(0)

    consignor_id = request.data.get('consignorId')
    category_id = request.data.get('categoryId')
    title = request.data.get('title')

    price = request.data.get('price', dzero)
    print('price', price)
    price = price if price else dzero
    print('price', price)

    retail_price = request.data.get('retailPrice', dzero)
    retail_price = retail_price if retail_price else dzero

    cost_net = request.data.get('costNet', dzero)
    cost_net = cost_net if cost_net else dzero

    quantity = request.data.get('quantity', 0)
    tag_quantity = request.data.get('tagQuantity', 0)

    item_fee = request.data.get('itemFee', dzero)
    item_fee = item_fee if item_fee else dzero

    allow_donate = request.data.get('allowDonate', False)
    featured_product = request.data.get('featuredProduct', False)

    shipping_handling = request.data.get('shippingHandling', dzero)
    shipping_handling = shipping_handling if shipping_handling else dzero

    web_fee = request.data.get('webFee', dzero)
    web_fee = web_fee if web_fee else dzero

    weight = request.data.get('weight', 0)
    width = request.data.get('width', 0)
    height = request.data.get('height', 0)
    date_received = request.data.get('dateReceived', datetime.datetime.now(datetime.timezone.utc))
    date_updated = datetime.datetime.now(datetime.timezone.utc)
    list_ready = request.data.get('listReady', False)
    post_date = datetime.datetime.now(datetime.timezone.utc)

    description = request.data.get('description', '')

    reseller = Reseller.objects.filter(pk=reseller_id).first()
    consignor = Consignor.objects.filter(pk=consignor_id).first()
    category = Category.objects.filter(pk=category_id).first()

    item = Item(
      reseller=reseller,
      consignor=consignor,
      category=category,
      title=title,
      price=price,
      retail_price=retail_price,
      cost_net=cost_net,
      quantity=quantity,
      tag_quantity=tag_quantity,
      item_fee=item_fee,
      allow_donate=allow_donate,
      featured_product=featured_product,
      shipping_handling=shipping_handling,
      web_fee=web_fee,
      weight=weight,
      width=width,
      height=height,
      date_received=date_received,
      list_ready=list_ready,
      post_date=post_date,
      date_updated=date_updated,
      status='NEW'
    )
      
    item.save()

    attributes = request.data.get('attributes')
    for a in attributes:
      a = json.loads(a)
      attribute_id = a['attributeId']
      attribute = Attributes.objects.filter(pk=attribute_id).first()
      ItemAttributes(reseller=reseller, item=item, attribute=attribute, value=a['value']).save()

    session = shopify.Session(reseller.domain, '2019-04', reseller.shopify_access_token)
    shopify.ShopifyResource.activate_session(session)
    new_product = shopify.Product()
    new_product.title = title
    new_product.product_type = category.json()['displayName']
    description = """
        <strong> {0} </strong>
        <br /><br />
        """.format(description)

    new_product.save()

    variant_object = {
            "product_id": new_product.id,
            "inventory_quantity": str(quantity),
            "price": str(price),
            "weight": weight
        }

    for a in attributes:
      a = json.loads(a)
      attribute_id = a['attributeId']
      attribute = Attributes.objects.filter(pk=attribute_id).first()
      new_product.add_metafield(shopify.Metafield({
        'namespace': 'attribute',
        'key': attribute.json()['name'],
        'value': a['value'],
        'value_type': 'string',
      }))
      variant_object[attribute.json()['name']] = a['value']
      description = """
        {0}
        <strong> {1} </strong>: {2}
        <br />
      """.format(description, attribute.json()['name'], a['value'])

    print(variant_object)
    variant = shopify.Variant(variant_object)
    variant.save()
    new_product.body_html = description
    new_product.add_variant(variant)
      
    new_product.save()

    

    return Response(status=status.HTTP_201_CREATED)


  
