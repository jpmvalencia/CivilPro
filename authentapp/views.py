from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from authentapp.models import Company, Degree, Employee, EmployeeDegree
from homeapp.views import proyectos_info

User = get_user_model()


def signin(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(request.user.username)
            return redirect(proyectos_info)

        # Si el usuario no es autenticado, muestra un mensaje de error o redirige a login
        return render(request, "login.html", {"error": "Credenciales invalidas"})


def signup_usu(request):
    if request.method == "GET":
        return render(request, "signup.html", {"degrees": Degree.objects.all()})
    else:
        if request.POST["password"] == request.POST["repassword"]:
            try:

                doc = request.POST["doc_id"]

                # Verificar si ya existe un empleado con el mismo doc
                if Employee.objects.filter(doc=doc).exists():
                    return render(
                        request,
                        "signup.html",
                        {
                            "degrees": Degree.objects.all(),
                            "error": "Ya existe un empleado con ese documento.",
                            "data": request.POST,
                        },
                    )

                username = request.POST["your_email"]
                password = request.POST["password"]
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                email = request.POST["your_email"]
                country_code = request.POST["code"]
                phone = request.POST["phone"]

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    country_code=country_code,
                    is_employee=True,
                )

                employee = Employee(
                    user=user,
                    doc=doc,
                )

                employee.save()

                degrees = request.POST.getlist("titles[]")
                for degree_name in degrees:
                    degree = Degree.objects.get(name=degree_name)
                    EmployeeDegree.objects.create(employee=employee, degree=degree)
                return redirect("../login")
            except Exception as e:
                print(e)
                return render(
                    request,
                    "signup.html",
                    {
                        "degrees": Degree.objects.all(),
                        "error": "Ya existe un usuario registrado con ese correo.",
                        "data": request.POST,
                    },
                )
        return render(
            request,
            "signup.html",
            {
                "degrees": Degree.objects.all(),
                "error": "Las contraseñas no coinciden.",
                "data": request.POST,
            },
        )


def signup_con(request):
    if request.method == "GET":
        return render(request, "signup-con.html")
    else:
        if request.POST["password"] == request.POST["repassword"]:
            try:
                nit = request.POST["nit_id"]
                if Company.objects.filter(nit=nit).exists():
                    return render(
                        request,
                        "signup-con.html",
                        {
                            "error": "Ya existe una compañía con ese NIT.",
                            "data": request.POST,
                        },
                    )
                username = request.POST["your_email"]
                name = request.POST["first_name"]
                email = request.POST["your_email"]
                password = request.POST["password"]
                country_code = request.POST["code"]
                phone = request.POST["phone"]

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=name,
                    phone=phone,
                    country_code=country_code,
                    is_company=True,
                )

                company = Company(
                    user=user,
                    nit=nit,
                )
                company.save()

                return redirect("../login")
            except Exception as e:
                return render(
                    request,
                    "signup-con.html",
                    {
                        "error": "Ya existe un usuario registrado con ese correo.",
                        "data": request.POST,
                    },
                )
        return render(
            request,
            "signup-con.html",
            {"error": "Las contraseñas no coinciden.", "data": request.POST},
        )


@login_required
def signout(request):
    logout(request)
    return redirect("/login")
