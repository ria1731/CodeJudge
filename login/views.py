from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Problem,Submission,TestCases,User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import subprocess
import docker
import os
from time import time
from django.conf import settings
from django.template import loader
# Create your views here.

######################################################################################################################################
# This is view for Home page
@login_required(login_url='Login')
def HomePage(request):
    #Pagination code
    problems = Problem.objects.order_by('id')
    paginator =Paginator(problems,7)
    page=request.GET.get('page')
    try:
        problems=paginator.page(page)
    except PageNotAnInteger:
        problems=paginator.page(1)
    except EmptyPage:
        problems=paginator.page(paginator.num_pages)
        

 
    # Sending dynamic data from DB to template.
    #problems=Problem.objects.all()
    return render(request,'login/home.html',{
            'problems':problems
        })

#######################################################################################################################################
# This is view for SignUP page
def SignUpPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)

            my_user.save()
            return redirect('Login')
    return render(request,'Login/signup.html')

####################################################################################################################################
# This is view for Login page
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            nu=User()
            nu.userName=username
            nu.password=pass1
            nu.save()

            login(request,user)
            return redirect('Home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render(request,'Login/login.html')

####################################################################################################################################
# This is view for logout page
@login_required(login_url='Login')
def LogOutPage(request):
    logout(request)
    return redirect('Login')

#####################################################################################################################################
# These are home page k baad wale views
@login_required(login_url='Login')
def P1(request,p_id):
    p=Problem.objects.get(pk=p_id)
    return render(request,'Home/P1.html',{
            'p':p
        })
    
#################################################################################################################################
# This is view for adding problem (jisko admin k through kr dia hai)
def addProblem(request):       
    if request.method=="POST":
        print("Data is coming")
        #fetch data
        problem_number=request.POST.get("problemNumber")
        problem_name=request.POST.get("problemName")
        problem_difficulty=request.POST.get("problemDifficulty")
        problem_description=request.POST.get("problemDescription")
        #create model object
        p=Problem()
        p.problemNumber=problem_number
        p.problemName=problem_name
        p.problemDifficulty=problem_difficulty
        p.problemDescription=problem_description
        #save the object
        p.save()
        return redirect("/home")
    else: return render(request,'Home/addProblem.html')

###################################################################################################################################
# This is view for Submission page
@login_required(login_url='Login')
def verdictPage(request, question_id):
    current_user = request.user

    # If you still want to use User.objects.get(), you can do it like this:
    try:
        current_user = User.objects.get(pk=current_user.id)
    except User.DoesNotExist:
        # Handle the case when the user is not found
        current_user = None

    

    if request.method == 'POST':
        # setting docker-client
        docker_client = docker.from_env()
        Running = "running"

        problem = Problem.objects.get(id=question_id)
        testcase = TestCases.objects.get(problem_id=question_id)
        # replacing \r\n by \n in original output to compare it with the usercode output
        testcase.output = testcase.output.replace('\r\n', '\n').strip()

        # score of a problem
        if problem.problemDifficulty == "easy":
            score = 10
        elif problem.problemDifficulty == "medium":
            score = 30
        else:
            score = 50

        # setting verdict to wrong by default
        verdict = "Wrong Answer"
        res = ""
        run_time = 0

        # extract data from form
        user_code = ''
        user_code = request.POST['user_code']
        user_code = user_code.replace('\r\n', '\n').strip()

        language = request.POST['language']
        submission = Submission(user=current_user, problem=problem)
        submission.save()

        filename = "Main"

        # if user code is in java
        extension = ".java"
        cont_name = "oj-java"
        compile = f"javac -o {filename} {filename}.java"
        clean = f"{filename} {filename}.java"
        docker_img = "openjdk"
        exe = f"./{filename}"

        file = filename + extension
        filepath = settings.FILES_DIR + "/" + file
        code = open(filepath, "w")
        code.write(user_code)
        code.close()

        # checking if the docker container is running or not
        try:
            container = docker_client.containers.get(cont_name)
            container_state = container.attrs['State']
            container_is_running = (container_state['Status'] == Running)
            if not container_is_running:
                subprocess.run(f"docker start {cont_name}", shell=True)
        except docker.errors.NotFound:
            subprocess.run(f"docker run -dt --name {cont_name} {docker_img}", shell=True)

        # copy/paste the .cpp file in docker container
        subprocess.run(f"docker cp {filepath} {cont_name}:/{file}", shell=True)

        # compiling the code
        cmp = subprocess.run(f"docker exec {cont_name} {compile}", capture_output=True, shell=True)
        if cmp.returncode != 0:
            verdict = "Compilation Error"
            subprocess.run(f"docker exec {cont_name} rm {file}", shell=True)

        else:
            # running the code on given input and taking the output in a variable in bytes
            start = time()
            try:
                res = subprocess.run(f"docker exec {cont_name} sh -c 'echo \"{testcase.input}\" | {exe}'",
                                     capture_output=True, timeout=2, shell=True)
                run_time = time() - start
                subprocess.run(f"docker exec {cont_name} rm {clean}", shell=True)
            except subprocess.TimeoutExpired:
                run_time = time() - start
                verdict = "Time Limit Exceeded"
                subprocess.run(f"docker container kill {cont_name}", shell=True)
                subprocess.run(f"docker start {cont_name}", shell=True)
                subprocess.run(f"docker exec {cont_name} rm {clean}", shell=True)

            if verdict != "Time Limit Exceeded" and res.returncode != 0:
                verdict = "Runtime Error"

        user_stderr = ""
        user_stdout = ""
        if verdict == "Compilation Error":
            user_stderr = cmp.stderr.decode('utf-8')

        elif verdict == "Wrong Answer":
            user_stdout = res.stdout.decode('utf-8')
            if str(user_stdout) == str(testcase.output):
                verdict = "Accepted"
            testcase.output += '\n'  # added extra line to compare user output having extra ling at the end of their output
            if str(user_stdout) == str(testcase.output):
                verdict = "Accepted"

        # creating Solution class objects and showing it on leaderboard
        # user = User.objects.get(username=request.user)
        # previous_verdict = Submission.objects.filter(user=user.id, problem=problem, verdict="Accepted")
        # if len(previous_verdict) == 0 and verdict == "Accepted":
        #     user.total_score += score
        #     user.total_solve_count += 1
        #     if problem.difficulty == "Easy":
        #         user.easy_solve_count += 1
        #     elif problem.difficulty == "Medium":
        #         user.medium_solve_count += 1
        #     else:
        #         user.tough_solve_count += 1
        #     user.save()
       # user = user_id
        user=User()
        user.score = user.score + score
        user.save()
        submission.result = verdict
        submission.user=current_user.id
        submission.save()
        os.remove(filepath)
        context = {'verdict': verdict}
        return render(request, 'Home/verdict.html', context)
      
##################################################################################################################################  
# This is view for Discuss page    
@login_required(login_url='Login')
def Discuss(request):
    return render(request,'Home/discuss.html') 

########################################################################################################################################
@login_required(login_url='Login')
def leaderBoard(request):
    mydata = User.objects.order_by('-score')[:10]
    paginator = Paginator(mydata, 10)
    page = request.GET.get('page')
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    template = loader.get_template("Home/leaderBoard.html")
    context = {
        'users': data,
    }
    return HttpResponse(template.render(context, request))

   
    
        



