from BeautifulSoup import BeautifulSoup
from requests import Request, Session
import getpass
import numpy as np
import matplotlib.pyplot as plt

GRADE_STRUCTURE = {'A+' : 4.3, 'A'  : 4, 'A-' : 3.7,
                   'B+' : 3.3, 'B': 3, 'B-' : 2.7,
                   'C+' : 2.3, 'C' : 2.0, 'C-' : 1.7,
                   'D+' : 1.3, 'D' : 1.0, 'D-'  : 0.7,
                   'F': 0}

GRADE_STRUCTURE_LIST = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-',
                        'D+', 'D', 'D-', 'F']

GRADES_INT = [4.3,4,3.7,3.3,3,2.7,2.3,2.0,1.7,1.3,1.0,0.7,0]

def scrapper():
    title = ""
    grades = list()
    nGrades = list()


    payoff = dict()
    loginURL = "https://my.concordia.ca/psp/upprpr9/?cmd=login&languageCd=ENG"
    mainURL = "https://my.concordia.ca/psc/upprpr9/EMPLOYEE/EMPL/s/WEBLIB_CONCORD.CU_SIS_INFO.FieldFormula.IScript_StudentGrades?PORTALPARAM_PTCNAV=CU_MY_CURRENT_GRADES&amp;EOPP.SCNode=EMPL&amp;EOPP.SCPortal=EMPLOYEE&amp;EOPP.SCName=CU_ACADEMIC&amp;EOPP.SCLabel=Academic&amp;EOPP.SCPTfname=CU_ACADEMIC&amp;FolderPath=PORTAL_ROOT_OBJECT.CU_ACADEMIC.CU_MY_CURRENT_GRADES&amp;IsFolder=false&amp;PortalActualURL=https%3a%2f%2fmy.concordia.ca%2fpsc%2fupprpr9%2fEMPLOYEE%2fEMPL%2fs%2fWEBLIB_CONCORD.CU_SIS_INFO.FieldFormula.IScript_StudentGrades&amp;PortalContentURL=https%3a%2f%2fmy.concordia.ca%2fpsc%2fupprpr9%2fEMPLOYEE%2fEMPL%2fs%2fWEBLIB_CONCORD.CU_SIS_INFO.FieldFormula.IScript_StudentGrades&amp;amp;PortalContentProvider=EMPL&amp;PortalCRefLabel=My%20Grades&amp;PortalRegistryName=EMPLOYEE&amp;PortalServletURI=https%3a%2f%2fmy.concordia.ca%2fpsp%2fupprpr9%2f&amp;PortalURI=https%3a%2f%2fmy.concordia.ca%2fpsc%2fupprpr9%2f&amp;PortalHostNode=EMPL&amp;NoCrumbs=yes&amp;PortalKeyStruct=yes"
    registerURL = "https://regsis.concordia.ca/portalRegora/undergraduate/wr215.asp"
    register = {}
    session = Session()

    print("-Login Credentials-")
    print("\n")
    userid = raw_input("Username:")
    pwd = getpass.getpass("Password:")
    payoff["userid"] = userid
    payoff["pwd"] = pwd

    post_request = Request('POST', loginURL, data=payoff)
    prepare_post = session.prepare_request(post_request)
    post_response = session.send(prepare_post)

    get_request = Request('GET', mainURL)
    prepare_get = session.prepare_request(get_request)
    get_response = session.send(prepare_get)

    soup = BeautifulSoup(get_response.text)

    for tr in soup.findAll('tr')[2:]:
        gradeDistArray = list()
        tds = tr.findAll('td')
        print "{} {}".format(tds[0].text , tds[1].text)
        title = tds[0].text
        yourGrade = tds[1].text
        grades.append(convert_to_GPA(str(tds[1].text)))
        for gradeDistValue in tr.findAll('td', attrs={'class':'cusistabledata'})[2:]:
                gradeDistArray.append(int(gradeDistValue.text))
        if (title != None) and (gradeDistArray) and (yourGrade != None):
            graphs(title, gradeDistArray, yourGrade)
    nGrades = np.array(removing_none(grades))
    print "Average this year: {}".format(nGrades.mean())

def calculator(*args):
    classGrades = []
    newClassGrades = []
    nClassGrades = []
    for i in args:
        classGrades = i.split(',')
    for z in classGrades:
        newClassGrades.append(convert_to_GPA(z))
    nClassGrades = np.array(removing_none(newClassGrades))
    print nClassGrades
    mu = nClassGrades.mean()
    print "Average Gpa: {0:.2f}".format(mu)

def graphs(title, gradeDistArray, yourGrade):
    x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13])
    otherX = [1,2,3,4,5,6,7,8,9,10,11,12]
    splitUp = list()
    nGradeDistArray = list()

    for i in range(0,12):
        z = 0
        while z != gradeDistArray[i]:
            nGradeDistArray.append(GRADES_INT[i])
            z = z + 1
    nGradeDistArray = np.array(nGradeDistArray)
    
    plt.xkcd()
    plt.title(title)
    plt.xlabel("Grade Distribution")
    plt.ylabel("Frequency")
    plt.xticks(x, GRADE_STRUCTURE_LIST)
    yourGradePos = [i for i,s in enumerate(GRADE_STRUCTURE_LIST) if s==yourGrade]
    for z in yourGradePos:
        yourGradeX = otherX[z]
        yourGradeY = gradeDistArray[z]
    plt.annotate('You', xy=(yourGradeX,yourGradeY), xytext=(yourGradeX+1,yourGradeY+1),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    mu = nGradeDistArray.mean()
    median = np.median(nGradeDistArray)
    
    plt.text(8, max(gradeDistArray)*0.85, 'Average of the class is:{0:.2f} \nMedian of the class is: {1:.2f} \nYour Grade: {2} | {3} '.format(mu, median, yourGrade,
                                                                                                                                          convert_to_GPA(yourGrade)))
    plt.plot(x, gradeDistArray)
    plt.show()
    

def convert_to_GPA(letter):
    if letter in GRADE_STRUCTURE:
        if (GRADE_STRUCTURE[letter] != None):
            return GRADE_STRUCTURE[letter]

def removing_none(List):
    return filter(lambda x: x is not None, List)
        
choice = raw_input("(G)rade Scrapper, Grade (C)alculator: ")
choice = choice.upper()

if (choice == "G"):
    scrapper()
elif (choice == "C"):
    grades = raw_input("Grade List: ")
    calculator(grades)
    
