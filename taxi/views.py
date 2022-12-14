from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CarForms, DriverCreationForm, DriverForm, CarSearchForm
from .models import Driver, Car, Manufacturer


def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(generic.ListView):
    model = Manufacturer
    template_name = "taxi/manufacturer_list.html"
    context_object_name = "manufacturer_list"
    paginate_by = 5


class ManufacturerDetailView(generic.DetailView):
    model = Manufacturer
    context_object_name = "manufacturer"


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    template_name = "taxi/manufacturer_confirm_delete.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(generic.ListView):
    model = Car
    template_name = "taxi/car_list.html"
    context_object_name = "car_list"
    paginate_by = 10
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        car_model = self.request.GET.get("car_model", "")
        context["search_form"] = CarSearchForm(initial={
            "car_model": car_model
        })

        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                model__icontains=form.cleaned_data["car_model"]
            )
        return self.queryset


class CarDetailView(generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForms
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForms
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_confirm_delete.html"


class DriverListView(generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateView(generic.UpdateView):
    model = Driver
    form_class = DriverForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"


@login_required
def car_assign_remove_view(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    car = Car.objects.get(id=pk)
    if car in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)

    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
