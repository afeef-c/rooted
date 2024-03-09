from django.conf import settings
from django.forms import inlineformset_factory
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from accounts.models import *
from .forms import CouponForm, OfferForm
from orders.models import Coupon, Order, OrderProduct, Payment
from store.models import *
from category.models import Category
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.mail import send_mail
from django.db.models import Sum
from django.db.models import F
from functools import wraps
from django.core.exceptions import PermissionDenied





def admin_required(view_func):
    """Decorator to restrict access to admin users only."""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied  # Or you can redirect to a different page or return an HttpResponseForbidden
        return view_func(request, *args, **kwargs)
    return _wrapped_view
def admin_required(view_func):
    """
    Decorator for views that checks whether the user is an admin.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

#============================Home =======================================================================


@login_required(login_url='admin_login')
@admin_required
def admin_home(request):

    if not request.user.is_admin:
        return redirect('admin_login')  # Redirect to the user dashboard if not a super admin


    orders_count = Order.objects.all().count()
    completed_orders = Order.objects.filter(status='Completed')
    confimed_orders = Order.objects.filter(status='Confirmed')
    delivered_orders = Order.objects.filter(status='Delivered')
    sales_count = OrderProduct.objects.all().count()

#-----------------------------------------------------
    total_revenue = 0
    payment = Payment.objects.filter(status='SUCCESS')
    for i in payment:
        total_revenue += float(i.amount_paid) 
#-----------------------------------------------------
    orders = orders = Order.objects.all().order_by('-created_at')
    top_oders = orders[:5]

    most_ordered_products = (
        OrderProduct.objects.values('product')  # Group by product name
        .annotate(total_quantity=Sum('quantity'))  # Calculate total quantity for each product
        .order_by('-total_quantity')  # Order by total quantity in descending order
        [:5]  # Limit to the top 5 most ordered products
    )
    top_five_most_ordered_products_details = Product.objects.filter(id__in=[item['product'] for item in most_ordered_products])
    
    most_ordered_category = (
        OrderProduct.objects.values('product__category__slug')  # Group by category name
        .annotate(total_quantity=Sum('quantity'))  # Calculate total quantity for each category
        .order_by('-total_quantity')  # Order by total quantity in descending order
        [:5]  # Fetch the top most ordered category
    )
    
    
    out_of_stock_products = Product.objects.all().order_by('stock')[:5]

#    most_ordered_category = [
#    {'category_name': item['product__category__cat_name'], 'total_quantity': item['total_quantity']} 
#    for item in most_ordered_category
#]
    
    top_five_most_ordered_categories_details = Category.objects.filter(slug__in=[item['product__category__slug'] for item in most_ordered_category]).prefetch_related('product_set')


#-----------------------------------------------------
    
    context ={
        'user': request.user,
        'orders_count':orders_count,
        'completed_orders':completed_orders,
        'confimed_orders':confimed_orders,
        'delivered_orders':delivered_orders,
        'sales_count':sales_count,
        'total_revenue':round(total_revenue,2),
        'orders':orders,
        'top_oders':top_oders,
        'most_ordered_products':most_ordered_products,
        'top_five_most_ordered_products_details':top_five_most_ordered_products_details,
        'out_of_stock_products':out_of_stock_products,
        'most_ordered_category':most_ordered_category,
        'top_five_most_ordered_categories_details':top_five_most_ordered_categories_details
        
    }

    return render(request,'customadmin/admin_home.html', context)




#============================Categories =======================================================================

@method_decorator(admin_required, name='dispatch')
class CategoriesListView(ListView):
    model = Category
    template_name = "customadmin/categories/category_list.html"
    context_object_name = "categories"

@method_decorator(admin_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class CategoriesCreate(SuccessMessageMixin, CreateView):
    model = Category
    success_message = "New category added!"
    fields = "__all__"
    template_name = "customadmin/categories/category_create.html"

@method_decorator(admin_required, name='dispatch')
class CategoriesUpdate(SuccessMessageMixin, UpdateView):
    model = Category
    success_message = " Category updated!"
    fields = "__all__"
    template_name = "customadmin/categories/category_update.html"
#====================================Users=================================================================================
@method_decorator(admin_required, name='dispatch')
class UsersListView(ListView):
    model = Account
    template_name = "customadmin/user_list.html"
    context_object_name = "users"

@method_decorator(admin_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class UserCreateView(SuccessMessageMixin, CreateView):
    model = Account
    template_name = "customadmin/user_create.html"
    fields = ['first_name','last_name','username','email','password','is_admin','is_active','is_merchant','is_staff','is_blocked']
    success_message = "New user added!"
    success_url = reverse_lazy('users_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        # Customize the success message based on the form data
        # You can access form.cleaned_data to retrieve form input values
        return f"User {cleaned_data['username']} created successfully."

@method_decorator(admin_required, name='dispatch')
@method_decorator(login_required, name='dispatch')    
class UserUpdate(SuccessMessageMixin, UpdateView):
    model = Account
    template_name = "customadmin/user_update.html"
    fields = ['first_name','last_name','username','email','password','is_admin','is_active','is_merchant','is_staff','is_blocked']
    success_message = "New user added!"
    success_url = reverse_lazy('users_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        return f"User {cleaned_data['username']} updated successfully."

@method_decorator(admin_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class UserDeleteView(SuccessMessageMixin,DeleteView):
    model = Account
    template_name = 'customadmin/user_delete.html'  
    success_message = " User {{user.ussername}} deleted!"
    success_url = reverse_lazy('users_list') 

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        return Account.objects.get(pk=user_id)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete User Account'
        return context
    
    def get_success_message(self, cleaned_data):
        return f"User deleteded successfully."

#============================================Products=======================================================================
@method_decorator(admin_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = "customadmin/products/product_list.html"
    context_object_name = "products"

@method_decorator(admin_required, name='dispatch')
class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    template_name = "customadmin/products/add_product.html"
    fields = '__all__'
    success_message = "New product added!"
    success_url = reverse_lazy('products_list') 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.all().order_by('cat_name')
        #form.fields['merchant'].queryset = Account.objects.filter(is_merchant=True)
        return form

    def form_valid(self, form):
        # Handle the creation of associated ProductImages
        images = self.request.FILES.getlist('images')
        for image in images:
            product_image = ProductImages(images=image, product=self.object)
            product_image.save()

        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return f"Product {cleaned_data['product_name']} created successfully."

@method_decorator(admin_required, name='dispatch')
class ProductUpdate(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = "customadmin/products/product_update.html"
    fields = '__all__'
    success_message = "The Product added!"
    success_url = reverse_lazy('products_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        return f"Product: {cleaned_data['product_name']} updated successfully."
    
@method_decorator(admin_required, name='dispatch')
class ProductDeleteView(SuccessMessageMixin, DeleteView):
    model = Product
    template_name = 'customadmin/products/product_delete.html'
    success_message = "Product {{ product.product_name }} deleted successfully!"
    success_url = reverse_lazy('products_list')

    def get_object(self, queryset=None):
        product_id = self.kwargs.get('pk')
        return Product.objects.get(pk=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Product'
        return context
#========================Product Images=============================================================================
@method_decorator(admin_required, name='dispatch')
class ProductImagesListView(ListView):
    template_name = "customadmin/products/product_images.html"
    context_object_name = "images"

    def get_queryset(self):
        # Get the product ID from the URL parameter or from the view's kwargs
        product_id = self.kwargs.get('product_id')  # Assuming the URL pattern includes 'product_id'
        # Fetch the queryset of ProductImages filtered by the product ID
        queryset = ProductImages.objects.filter(product_id=product_id)
        return queryset
    

#@method_decorator(login_required, name='dispatch')
#class ProductImagesCreateView(SuccessMessageMixin, CreateView):
#    model = ProductImages
#    template_name = "customadmin/products/product_images.html"
#    fields = '__all__'
#    success_message = "New Images added!"
#    success_url = reverse_lazy('products_list') 


#    def form_valid(self, form):
#        # Save the product instance
#        self.object = form.save()

#        # Handle the creation of associated ProductImages
#        images = self.request.FILES.getlist('images')
#        for image in images:
#            product_image = ProductImages(images=image, product=self.object)
#            product_image.save()

#        return super().form_valid(form)


#    def get_success_message(self, cleaned_data):
#        return f"Product {cleaned_data['product_name']} created successfully."


def add_product_images(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    ProductImageFormSet = inlineformset_factory(Product, ProductImages, fields=('images',), extra=3)  # Allow adding up to 3 images
    
    if request.method == 'POST':
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if formset.is_valid():
            formset.save()
            return redirect('products_list')  # Redirect to product list after successful submission
    else:
        formset = ProductImageFormSet(instance=product)

    return render(request, 'customadmin/products/product_images.html', {'formset': formset})
#========================Variations=============================================================================
class VariationtListView(ListView):
    model = Variation
    template_name = "customadmin/products/variation_list.html"
    context_object_name = "variations"

@method_decorator(login_required, name='dispatch')
class VariationCreateView(SuccessMessageMixin, CreateView):
    model = Variation
    template_name = "customadmin/products/add_variations.html"
    fields = '__all__'
    success_message = "New variations added!"
    success_url = reverse_lazy('variations_list') 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['product'].queryset = Product.objects.all().order_by('product_name')
        return form


    def get_success_message(self, cleaned_data):
        return f"Variattion created successfully."

@method_decorator(login_required, name='dispatch')
class VariationUpdate(SuccessMessageMixin, UpdateView):
    model = Variation
    template_name = "customadmin/products/variation_update.html"
    fields = '__all__'
    success_message = "The Variation updated!"
    success_url = reverse_lazy('variations_list') 

    def form_valid(self, form):

        responce = super().form_valid(form)

        return responce
    def get_success_message(self, cleaned_data):
        return f"Variation updated successfully."


@method_decorator(login_required, name='dispatch')
class VariationDeleteView(SuccessMessageMixin, DeleteView):
    model = Variation
    template_name = 'customadmin/products/variation_delete.html'
    success_message = "Variation  deleted successfully!"
    success_url = reverse_lazy('variations_list')

    def get_object(self, queryset=None):
        variation_id = self.kwargs.get('pk')
        try:
            variation = Variation.objects.get(pk=variation_id)
        except Variation.DoesNotExist:
            raise Http404("Variation does not exist")
        return variation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Variation'
        return context

#============================================Order Management=======================================================================
class OrderListView(ListView):
    model = Order
    template_name = "customadmin/orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        # Get the queryset of orders and order them by date in ascending order
        return Order.objects.all().order_by('-created_at')



@method_decorator(login_required, name='dispatch')
class OrderUpdate(SuccessMessageMixin, UpdateView):
    model = Order
    template_name = "customadmin/orders/order_update.html"
    fields = '__all__'
    success_message = "The order status updated!"
    success_url = reverse_lazy('orders_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        orders_emails = order.email 
        context['orders_emails'] = orders_emails
        return context

    def form_valid(self, form):
        # Call the parent class's form_valid method
        response = super().form_valid(form)

        # Check if there's an update in order status
        if form.has_changed() and 'status' in form.changed_data:
            # Get the updated order object
            order = self.object
            # Get the customer email from the order
            customer_email = order.email
            # Compose the email message
            subject = 'Order Status Update'
            message = f'Your Order status has been updated to: {order.status}'
            sender_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [customer_email]
            # Send the email
            send_mail(subject, message, sender_email, recipient_list)

        return response
    
    def get_success_message(self, cleaned_data):
        order_number = cleaned_data.get('order_number', '')  # Assuming 'order_number' is a field of the form
        name = cleaned_data.get('full_name', '')  # Assuming 'full_name' is a field of the form
        return f"Order: {name}-{order_number} updated successfully."
    


#============================================ Paymment =======================================================================
class PaymentListView(ListView):
    model = Payment
    template_name = "customadmin/orders/payment_list.html"
    context_object_name = "payments"

    def get_queryset(self):
        # Get the queryset of orders and order them by date in ascending order
        return Payment.objects.all().order_by('-created_at')



@method_decorator(login_required, name='dispatch')
class PaymentUpdate(SuccessMessageMixin, UpdateView):
    model = Payment
    template_name = "customadmin/orders/payment_update.html"
    fields = '__all__'
    success_message = "The order updated!"
    success_url = reverse_lazy('payment_list') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment = self.get_object()
        # Assuming there can be multiple orders associated with a payment
        orders_emails = [order.email for order in payment.order_set.all()]
        context['orders_emails'] = orders_emails
        return context

    def form_valid(self, form):
        # Call the parent class's form_valid method
        response = super().form_valid(form)

        # Check if there's an update in payment status
        if form.has_changed() and 'status' in form.changed_data:
            # Get the updated payment object
            payment = self.object
            # Access the related customer's email (assuming Payment model has a foreign key to Customer)
            customer_email = [order.email for order in payment.order_set.all()]
            # Compose the email message
            subject = 'Payment Status Update'
            message = f'Your payment status has been updated to: {payment.status}'
            sender_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [order.email for order in payment.order_set.all()]
            # Send the email
            send_mail(subject, message, sender_email, recipient_list)

        return response

    
    def get_success_message(self, cleaned_data):
        payment_id = self.object.id  # Access the payment's unique identifier
        return f"Payment {payment_id} updated successfully."
    

#============================================ Offers =======================================================================
class CategoryOffers(ListView):
    model = CategoryOffer
    template_name = "customadmin/offersandcoupons/category_offers.html"
    context_object_name = "offers"

class ProductOffers(ListView):
    model = Offer
    template_name = "customadmin/offersandcoupons/product_offers.html"
    context_object_name = "offers"


@method_decorator(login_required, name='dispatch')
class ProductOfferCreateView(SuccessMessageMixin, CreateView):
    model = Offer
    success_message = "New product offer added!"
    fields = "__all__"
    template_name = "customadmin/offersandcoupons/add_product_offers.html"
    success_url = reverse_lazy('product_offers') 

    def form_valid(self, form):
        
        #category_id = form.cleaned_data.get('category').id
        #product_id = form.cleaned_data.get('product').id
        start_date = form.cleaned_data.get('start_date')  # Assuming start_date is a field in your form
        end_date = form.cleaned_data.get('end_date')  # Assuming end_date is a field in your form


        if start_date > end_date:
            messages.error(self.request, "Start date cannot be greater than end date.")
            return redirect('product_offers')  # Redirect to a different page or adjust as needed

        
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CategoryOfferCreateView(SuccessMessageMixin, CreateView):
    model = CategoryOffer
    success_message = "New category offer added!"
    fields = "__all__"
    template_name = "customadmin/offersandcoupons/add_category_offers.html"
    success_url = reverse_lazy('category_offers') 
    


    def form_valid(self, form):
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        if start_date > end_date:
            messages.error(self.request, "Start date cannot be greater than end date.")
            return redirect('category_offers')  # Redirect to a different page or adjust as needed

        category_id = form.cleaned_data.get('category').id
        existing_offer = CategoryOffer.objects.filter(category_id=category_id).exists()

        if existing_offer:
            messages.error(self.request, "An offer already exists for this category.")
            return redirect('category_offers')  # Redirect to a different page or adjust as needed
        
        return super().form_valid(form)

    def save(self, *args, **kwargs):
        # Ensure discount_percentage is within certain limits
        max_discount_percentage = 90  # Example: Maximum allowed discount percentage
        min_discount_percentage = 0   # Example: Minimum allowed discount percentage
        if self.discount_percentage > max_discount_percentage:
            self.discount_percentage = max_discount_percentage
        elif self.discount_percentage < min_discount_percentage:
            self.discount_percentage = min_discount_percentage
        
        # Check if the end_date is greater than the start_date
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")

        # Your existing save logic...
        
        super().save(*args, **kwargs)
    




@method_decorator(login_required, name='dispatch')
class CategoryOffersUpdate(SuccessMessageMixin, UpdateView):
    model = CategoryOffer
    template_name = "customadmin/offersandcoupons/category_offers_update.html"
    fields = '__all__'
    success_message = "The Offers status updated!"
    success_url = reverse_lazy('category_offers') 

    def form_valid(self, form):
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            if start_date > end_date:
                messages.error(self.request, "Start date cannot be greater than end date.")
                return self.form_invalid(form)  # Return form invalid if start date is greater than end date
            
            return super().form_valid(form)
    
    def get_success_message(self, cleaned_data):
        name = cleaned_data.get('product')  # Assuming 'order_number' is a field of the form
        
        return f"Product:{name} offer  updated successfully."

    

@method_decorator(login_required, name='dispatch')
class ProductOffersUpdate(SuccessMessageMixin, UpdateView):
    model = Offer
    template_name = "customadmin/offersandcoupons/product_offers_update.html"
    fields = '__all__'
    success_message = "The Offers status updated!"
    success_url = reverse_lazy('product_offers') 

    def form_valid(self, form):
        start_date = form.cleaned_data.get('start_date')  # Assuming start_date is a field in your form
        end_date = form.cleaned_data.get('end_date')  # Assuming end_date is a field in your form

        if start_date > end_date:
            messages.error(self.request, "Start date cannot be greater than end date.")
            return redirect('product_offers')  # Redirect to a different page or adjust as needed
  
        
        response = super().form_valid(form)
        return response





#============================================ coupon =======================================================================
    
class Coupons(ListView):
    model = Coupon
    template_name = "customadmin/offersandcoupons/coupons.html"
    context_object_name = "coupons"


@method_decorator(login_required, name='dispatch')
class CouponCreateView(SuccessMessageMixin, CreateView):
    model = Coupon
    success_message = "New discount coupon added!"
    fields = "__all__"
    template_name = "customadmin/offersandcoupons/add_coupon.html"
    success_url = reverse_lazy('coupons') 



@login_required
def update_coupon(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "The discount coupon has been updated!")
            return redirect('coupons')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'customadmin/offersandcoupons/update_coupon.html', {'form': form, 'coupon': coupon})




@method_decorator(login_required, name='dispatch')
class CouponDeleteView(SuccessMessageMixin, DeleteView):
    model = Coupons
    template_name = "customadmin/offersandcoupons/delete_coupon.html"
    success_message = "The discount coupon deleted successfully!"
    success_url = reverse_lazy('coupons')


    def get_object(self, queryset=None):
        coupon_id = self.kwargs.get('pk')
        return Coupon.objects.get(pk=coupon_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Coupon'
        return context
#======================================================================================================================================