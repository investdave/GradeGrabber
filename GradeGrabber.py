
from BeautifulSoup import BeautifulSoup
from requests import Request, Session
import getpass
import numpy as np

GRADE_STRUCTURE = {'A+' : 4.3, 'A'  : 4, 'A-' : 3.7,
                   'B+' : 3.3, 'B': 3, 'B-' : 2.7,
                   'C+' : 2.3, 'C' : 2.0, 'C-' : 1.7,
                   'D+' : 1.3, 'D' : 1.0, 'D-'  : 0.7,
                   'F': 0}





def scrapper():
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

    #post_request = Request('POST', registerURL, data=

    soup = BeautifulSoup(get_response.text)

    for tr in soup.findAll('tr'):
        tds = tr.findAll('td')
        print tds[0].text , tds[1].text
        if tds[1].text in GRADE_STRUCTURE:
            grades.append(GRADE_STRUCTURE[tds[1].text])
    
        nGrades = np.array(grades)
    print "Average this year: {}".format(nGrades.mean())

def calculator(*args):
    classGrades = []
    newClassGrades = []
    nClassGrades = []
    for i in args:
        classGrades = i.split(',')
    for z in classGrades:
        newClassGrades.append(GRADE_STRUCTURE[z])
    nClassGrades = np.array(newClassGrades)
    print nClassGrades
    mu = nClassGrades.mean()
    print "Average Gpa: {0:.2f}".format(mu)

choice = raw_input("(G)rade Scrapper, Grade (C)alculator: ")

if (choice == "G"):
    scrapper()
elif (choice == "C"):
    grades = raw_input("Grade List: ")
    calculator(grades)
    
