""" Import statements """
import flask
import subprocess
import re
""" Global/state variables """
app = flask.Flask(__name__)
MAX_RETURN = 50


""" Pre-compiled regex patterns for metadata """
coursere = re.compile(r"\ntitle: (.*)\n")
partre = re.compile(r"\ncourse_year: (.*)\n")
yearre = re.compile(r"\ndate: (.*)\n")

def metadata(file):
    """ Get metadata from markdown file header """
    print(file)
    with open(file,"r") as raw:
        raw = raw.read()
        course = re.search(coursere,raw)
        part = re.search(partre,raw)
        year = re.search(yearre,raw)
        check = lambda s: "" if s is None else s.group(1)
        return {"course": check(course), "part": check(part), "year": check(year), "id": file[5:-3]}
        
""" Server routes """
@app.route("/",methods=["GET"])
def home_route():
    """ Return static home page HTML """
    return flask.send_file("web/home.html")

@app.route("/search",methods=["GET"])
def search_route():
    """ Return the matching questions for a search """
    query = flask.request.args.get("query")
    course = flask.request.args.get("course")
    if query is not None:
        res = subprocess.run(["grep","-rl",f"{query}","data"],text=True,capture_output=True)
        if res.returncode != 0:
            return {}
        else:
            files = res.stdout.split("\n")
            json = []
            for file in files:
                if file == "": continue
                meta = metadata(file)
                if meta is not None and (course == "all" or meta["course"]== course) :
                    json.append(meta)
            return {"results": json[:MAX_RETURN]}
    else: return {} 


@app.route("/pdf",methods=["GET"])
def pdf_route():
    """ Return the generated pdf file for a question id """
    qid = flask.request.args.get("id")
    if qid is not None:
        return flask.send_file(f"pdf/{qid}.pdf")
    else:
        return {}

