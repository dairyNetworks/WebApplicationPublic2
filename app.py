from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend import query_module_combined
from backend import query_doc
from backend import query_module
from backend import network_com
from backend import network_query
from backend import get_action_table
from backend import get_fv_table
from backend import get_fvr_table
from backend import get_fw_table
from backend import get_action_plan
from backend import get_action_plan_network
from backend import get_fv
from backend import get_fv_network
from backend import get_fvr
from backend import get_fvr_network
from backend import get_fvr_report
from backend import get_fvr_report_network
from backend import get_fw_network
from backend import get_fw
from backend import get_sentiment_network
from backend import get_sentiment
from backend import get_primary_stakeholders
from backend import get_secondary_stakeholder
from backend import get_secondary_stakeholder_network
from backend import get_actionstakeholder_table
from backend import get_actionstakeholder_plan
from backend import get_actionstakeholder_plan_network
from backend import get_fvstakeholder_table
from backend import get_fvstakeholder_plan
from backend import get_fvstakeholder_network
from backend import get_fwstakeholder_table
from backend import get_fwstakeholder_plan
from backend import get_fwstakeholder_plan_network
from backend import get_complete_network
from backend import get_complete_network_table
import uvicorn
import json
import time
from pathlib import Path
from fastapi import FastAPI
app = FastAPI()

templates = Jinja2Templates(directory="docs")

# Optional: Serve static files if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/manual", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("manual.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
async def home(request: Request, access: str = ""):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "access": access
    })

@app.get("/search", response_class=HTMLResponse)
async def read_search(request: Request, access: str = ""):
    return templates.TemplateResponse("search.html", {
        "request": request,
        "access": access
    })

@app.get("/network", response_class=HTMLResponse)
async def network_page(request: Request, access: str = ""):
    return templates.TemplateResponse("network.html", {
        "request": request,
        "access": access
    })

@app.get("/networkquery", response_class=HTMLResponse)
async def networkquery_page(request: Request):
    return templates.TemplateResponse("networkquery.html", {"request": request})

@app.get("/actionquery", response_class=HTMLResponse)
async def networkquery_page(request: Request):
    return templates.TemplateResponse("actionquery.html", {"request": request})

@app.get("/actionplan.html", response_class=HTMLResponse)
async def load_action_plan_page(request: Request, query: str, file_name: str, action: str):
    return templates.TemplateResponse("actionplan.html", {
        "request": request,
        "query": query,
        "file_name": file_name,
        "action": action
    })

@app.get("/foodvision.html", response_class=HTMLResponse)
async def load_fv_page(request: Request, query: str, action: str):
    return templates.TemplateResponse("foodvision.html", {
        "request": request,
        "query": query,
        "action": action
    })

@app.get("/foodvisionreportstake.html", response_class=HTMLResponse)
async def load_fv_stake_page(request: Request, query: str, action: str):
    return templates.TemplateResponse("foodvisionreportstake.html", {
        "request": request,
        "query": query,
        "action": action
    })

@app.get("/foodvisionreport.html", response_class=HTMLResponse)
async def load_fvr_page(request: Request, query: str, action: str):
    return templates.TemplateResponse("foodvisionreport.html", {
        "request": request,
        "query": query,
        "action": action
    })

@app.get("/foodwise.html", response_class=HTMLResponse)
async def load_fw_page(request: Request, query: str, recommendation: str, action: str):
    return templates.TemplateResponse("foodwise.html", {
        "request": request,
        "recommendation": recommendation,
        "action" : action
        })

@app.get("/sentimentstats", response_class=HTMLResponse)
async def sentimentstats_page(request: Request):
    return templates.TemplateResponse("sentimentstats.html", {"request": request})

@app.get("/completenetwork", response_class=HTMLResponse)
async def completenetwork_page(request: Request, access: str):
    return templates.TemplateResponse("completenetwork.html", {"request": request, "access": access})

@app.get("/completenetlabels", response_class=HTMLResponse)
async def completenetlabels_page(request: Request, category: str, access: str):
    return templates.TemplateResponse("completenetlabels.html", {"request": request, "access": access, "category": category})

@app.get("/completenetstakeholders", response_class=HTMLResponse)
async def completenetstakeholders_page(request: Request, access: str, label: str):
    return templates.TemplateResponse("completenetstakeholders.html", {"request": request, "access": access, "label": label})

@app.get("/get_complete_network_graph.html", response_class=HTMLResponse)
async def get_complete_network_graph_page(request: Request, access: str, label: str, query: str):
    return templates.TemplateResponse("get_complete_network_graph.html", {"request": request, "access": access, "label": label, "query" : query})

#@app.get("/get_query", response_class=HTMLResponse)
#async def get_complete_tables_page(request: Request, access: str, label: str, query: str):
#    return templates.TemplateResponse(
#        "get_query",
#        {
#            "request": request,
#            "access": access,
#            "label": label,
#            "query": query
#        }
#    )

@app.get("/speakersentiment.html", response_class=HTMLResponse)
async def load_fw_page(request: Request, query: str, category: str, sentiment: str):
    return templates.TemplateResponse("speakersentiment.html", {
        "request": request,
        "category": category,
        "sentiment" : sentiment
        })

@app.get("/stakeholdermapping", response_class=HTMLResponse)
async def stakeholdermapping_page(request: Request):
    return templates.TemplateResponse("stakeholdermapping.html", {"request": request})

@app.get("/secondarystakeholder.html", response_class=HTMLResponse)
async def secondarystakeholder_page(request: Request, query: str, primaryStakeholder : str):
    return templates.TemplateResponse("secondarystakeholder.html", {
        "request": request,
        "query": query,
        "primaryStakeholder" : primaryStakeholder
    })

@app.get("/networkfirst", response_class=HTMLResponse)
async def networkfirst_page(request: Request):
    return templates.TemplateResponse("networkfirst.html", {"request": request})


@app.get("/actionstakeholder", response_class=HTMLResponse)
async def actionstakeholder_page(request: Request):
    return templates.TemplateResponse("actionstakeholder.html", {"request": request})

@app.get("/actionstakeholderlist.html", response_class=HTMLResponse)
async def load_actionstakeholderlist_page(request: Request, query: str, formalStakeholder: str):
    return templates.TemplateResponse("actionstakeholderlist.html", {
        "request": request,
        "query": query,
        "formalStakeholder": formalStakeholder
    })

@app.get("/foodvisionstakeholder.html", response_class=HTMLResponse)
async def load_foodvisionstakeholder_page(request: Request, query: str, formalStakeholder: str):
    return templates.TemplateResponse("foodvisionstakeholder.html", {
        "request": request,
        "query": query,
        "formalStakeholder": formalStakeholder
    })

@app.get("/foodwisestakeholder.html", response_class=HTMLResponse)
async def load_foodwisestakeholder_page(request: Request, query: str, formalStakeholder: str):
    return templates.TemplateResponse("foodwisestakeholder.html", {
        "request": request,
        "query": query,
        "formalStakeholder": formalStakeholder
    })

@app.get("/search/speaker", response_class=HTMLResponse)
async def search_speaker(request: Request, keywords: str = Query(..., description="Keywords to search for"), access: str = Query(...)):
    try:
        # Run the query to get top documents
        results = query_module_combined.function_call_combined(keywords, access)

        # Normalize keyword list for identifying relevant fields
        if 'OR' in keywords:
            keyword_list = [k.strip().replace(' ', '_') for k in keywords.split('OR')]
        elif 'AND' in keywords:
            keyword_list = [k.strip().replace(' ', '_') for k in keywords.split('AND')]
        else:
            keyword_list = [keywords.strip().replace(' ', '_')]

        # Format results for display in HTML
        formatted_results = [
            {
                "Sliding_year": result.get("Sliding_year", "N/A"),
                "Organisation": result.get("Organization", "N/A"),
                "Designation": result.get("Designation", "N/A"),
                #"Region or Stakeholder Category": result.get("Region or Stakeholder Category", "N/A"),
                "TotalFrequency": result.get("TotalFrequency", 0),
                "Keywords": ', '.join([
                    f"{key}: {result.get(key)}"
                    for key in keyword_list
                    if key in result
                ])
            }
            for result in results if "Labels" in result and "Sliding_year" in result
        ]

        return templates.TemplateResponse("speakerresult.html", {
            "request": request,
            "search_keywords": keywords,
            "results": formatted_results
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/search/document")
async def search_document(request: Request, keywords: str = Query(..., description="Keywords to search for")):
    try:
        results = query_doc.function_call(keywords)
        
        formatted_results = []
        for result in results:
            if "File Name" in result:
                keywords_dict = {k: v for k, v in result.items() if k not in ["File Name", "_id"]}
                keywords_str = ', '.join([f"{key}: {value}" for key, value in keywords_dict.items()])
                formatted_results.append({
                    "File Name": result["File Name"],
                    "Keywords": keywords_str
                })
        
        return templates.TemplateResponse("documentresult.html", {
            "request": request, 
            "results": formatted_results,
            "search_keywords": keywords
        })
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/speaker/details", response_class=HTMLResponse)
async def speaker_details(request: Request, keywords: str = Query(...), speaker: str = Query(...)):
    try:
        # Call the backend function for speaker details
        results = query_module.function_call_speaker(keywords, speaker)

        # Check if the results are empty
        if not results:
            return templates.TemplateResponse("speakerdetail.html", {
                "request": request,
                "keywords": keywords,
                "speaker": speaker,
                "results": None
            })
        
        # Render the details template with results
        return templates.TemplateResponse("speakerdetail.html", {
            "request": request,
            "keywords": keywords,
            "speaker": speaker,
            "results": results
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/get_network")
async def get_network():
    try:
        data = network_com.fetch_network_data()
        return JSONResponse(content=data)
    except Exception as e:
        print("Error in /get_network:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/get_network_graph")
async def get_network_graph(request: Request, query: str = Query(...)):
    try:
        print('Query:', query)
        graph_data = network_query.get_network_data(query)  # Existing network data
        table_data = network_query.get_table_data()         # New table data
        return JSONResponse(content={
            "graph": graph_data,
            "table": table_data
        })
    except Exception as e:
        print(f"Error fetching network data: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.get("/get_action_table")
async def get_action_table_route(request: Request, query: str = Query(...),access: str = Query(...)):
    try:
        print('Query:', query)
        table_data = get_action_table.get_action_table(query,access) 
        return {"table": table_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/get_fv_table")
async def get_fv_table_route(request: Request, query: str = Query(...),access: str = Query(...)):
    try:
        print('Query:', query)
        table_data = get_fv_table.get_fv_table(query,access) 
        return {"table": table_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/get_fvr_table")
async def get_fvr_table_route(request: Request, query: str = Query(...),access: str = Query(...)):
    try:
        print('Query:', query)
        table_data = get_fvr_table.get_fvr_table(query,access) 
        return {"table": table_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/get_fw_table")
async def get_fw_table_route(request: Request, query: str = Query(...),access: str = Query(...)):
    try:
        print('Query:', query)
        table_data = get_fw_table.get_fw_table(query,access) 
        return {"table": table_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/get_action_plan")
async def get_action_plan_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    file_name: str = Query(..., description="Name of the action plan file"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('File Name:', file_name)
        print('Action:', action)
        table_data = get_action_plan.get_action_plan(query, file_name, action,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/get_action_plan_network")
async def get_action_plan_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    file_name: str = Query(..., description="Name of the action plan file"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('File Name:', file_name)
        print('Action:', action)
        graph_data = get_action_plan_network.get_action_plan_network(query, file_name, action,access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/get_fv")
async def get_fv_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)

):
    try:
        print('Query:', query)
        print('Action:', action)
        table_data = get_fv.get_fv(query, action,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/get_fv_network")
async def get_fv_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)

):
    try:
        print('Query:', query)
        print('Action:', action)
        graph_data = get_fv_network.get_fv_network(query, action, access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/get_fvr")
async def get_fvr_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('Action:', action)
        table_data = get_fvr.get_fvr(query, action,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/get_fvr_network")
async def get_fvr_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('Action:', action)
        graph_data = get_fvr_network.get_fvr_network(query, action,access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/get_fvr_report")
async def get_fvr_report_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('Action:', action)
        table_data = get_fvr_report.get_fvr_report(query, action, access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/get_fvr_report_network")
async def get_fvr_report_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    action: str = Query(..., description="Name of the action"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('Action:', action)
        graph_data = get_fvr_report_network.get_fvr_report_network(query, action, access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_fw")
async def get_fw_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    recommendation: str = Query(..., description="Name of the recommendation"),
    action: str = Query(...),
    access: str = Query(...)
):
    try:
        print('FW Query:', query)
        print('Action:',action)
        table_data = get_fw.get_fw(query, recommendation, action,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/get_fw_network")
async def get_fw_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    recommendation: str = Query(..., description="Name of the recommendation"),
    action: str = Query(...),
    access: str = Query(...)
    ):
    try:
        print('FW Query Network:', query)
        print('Action:',action)
        graph_data = get_fw_network.get_fw_network(query,recommendation, action,access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_sentiment")
async def get_sentiment_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    category: str = Query(..., description="Query category"),
    sentiment: str = Query(..., description="Query sentiment"),
    access: str = Query(...)
    ):
    try:
        print('Sentiment Query Network:', query)
        print('Category: ', category)
        print('Sentiment: ', sentiment)
        table_data = get_sentiment.get_sentiment(query, category, sentiment,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/get_sentiment_network")
async def get_sentiment_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    category: str = Query(..., description="Query category"),
    sentiment: str = Query(..., description="Query sentiment"),
    access: str = Query(...)
    ):
    try:
        print('Sentiment Query Network:', query)
        print('Category: ', category)
        print('Sentiment: ', sentiment)
        graph_data = get_sentiment_network.get_sentiment_network(query, category, sentiment, access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/get_primary_stakeholders")
async def get_primary_stakeholders_route(
    request: Request,
    query: str = Query(..., description="Query identifier Document Name'"),
    access: str = Query(...)
    ):
    try:
        print('Sentiment Query Network:', query)
        primary_stakeholders = get_primary_stakeholders.get_primary_stakeholders(query,access)
        print("Primary Stakeholders:", primary_stakeholders)
        return JSONResponse(content={
            "stakeholders": primary_stakeholders
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
   
@app.get("/get_secondary_stakeholder")
async def get_secondary_stakeholder_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    primaryStakeholder : str = Query(..., description="Query primaryStakeholder"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('Primary Stakeholder:', primaryStakeholder)
        table_data = get_secondary_stakeholder.get_secondary_stakeholder(query, primaryStakeholder,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_secondary_stakeholder_network")
async def get_secondary_stakeholder_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    primaryStakeholder : str = Query(..., description="Query primaryStakeholder"),
    access: str = Query(...)
    ):
    try:
        print('Sentiment Query Network:', query)
        print('Primary Stakeholder:', primaryStakeholder)
        graph_data = get_secondary_stakeholder_network.get_secondary_stakeholder_network(query, primaryStakeholder,access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_actionstakeholder_table")
async def get_actionstakeholder_table_route(request: Request, query: str = Query(...), access: str = Query(...)):
    try:
        print('Query:', query)
        table_data = get_actionstakeholder_table.get_actionstakeholder_table(query, access) 
        return {"table": table_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
   
@app.get("/get_actionstakeholder_plan")
async def get_actionstakeholder_plan_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    formalStakeholder: str = Query(..., description="Name of the formalStakeholder"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('formalStakeholder:', formalStakeholder)
        print('access: ',access)
        table_data = get_actionstakeholder_plan.get_actionstakeholder_plan(query,formalStakeholder,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
   
@app.get("/get_actionstakeholder_plan_network")
async def get_actionstakeholder_plan_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    formalStakeholder: str = Query(..., description="Name of the formalStakeholder"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('formalStakeholder:', formalStakeholder)
        print('access: ',access)
        graph_data = get_actionstakeholder_plan_network.get_actionstakeholder_plan_network(query, formalStakeholder,access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_fvstakeholder_table")
async def get_fvstakeholder_table_route(request: Request, query: str = Query(...), access: str = Query(...)):
    try:
        print('Query:', query)
        table_data = get_fvstakeholder_table.get_fvstakeholder_table(query, access) 
        return {"table": table_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
   
@app.get("/get_fvstakeholder_plan")
async def get_fvstakeholder_plan_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    formalStakeholder: str = Query(..., description="Name of the formalStakeholder"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('formalStakeholder:', formalStakeholder)
        print('access: ',access)
        table_data = get_fvstakeholder_plan.get_fvstakeholder_plan(query,formalStakeholder,access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
  
@app.get("/get_fvstakeholder_network")
async def get_fvstakeholder_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    formalStakeholder: str = Query(..., description="Name of the formalStakeholder"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('formalStakeholder:', formalStakeholder)
        graph_data = get_fvstakeholder_network.get_fvstakeholder_network(query, formalStakeholder,access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_fwstakeholder_table")
async def get_fwstakeholder_table_route(request: Request, query: str = Query(...), access: str = Query(...)):
    try:
        print('Query:', query)
        table_data = get_fwstakeholder_table.get_fwstakeholder_table(query, access) 
        return {"table": table_data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

   
@app.get("/get_fwstakeholder_plan")
async def get_fwstakeholder_plan_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    formalStakeholder: str = Query(..., description="Name of the formalStakeholder"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('formalStakeholder:', formalStakeholder)
        table_data = get_fwstakeholder_plan.get_fwstakeholder_plan(query,formalStakeholder, access)
        return JSONResponse(content={
            "table": table_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
  
@app.get("/get_fwstakeholder_plan_network")
async def get_fwstakeholder_plan_network_route(
    request: Request,
    query: str = Query(..., description="Query identifier like 'car', 'wat', or 'liv'"),
    formalStakeholder: str = Query(..., description="Name of the formalStakeholder"),
    access: str = Query(...)
):
    try:
        print('Query:', query)
        print('formalStakeholder:', formalStakeholder)
        graph_data = get_fwstakeholder_plan_network.get_fwstakeholder_plan_network(query, formalStakeholder,access)
        print("Graph Data:", graph_data)
        return JSONResponse(content={
            "graph": graph_data
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


import traceback

@app.get("/get_complete_network")
async def get_complete_network_route(
    request: Request,
    label: str = Query(..., description="Stakeholder label"),
    query: str = Query(..., description="Topic filter")
):
    try:
        print("⚡ Incoming request to /get_complete_network")
        graph_data = get_complete_network.get_complete_network(label, query)
        return JSONResponse(content={"graph": graph_data})

    except Exception as e:
        print("❌ Exception occurred in FastAPI route:")
        traceback.print_exc()  # full stack trace in terminal
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/get_complete_network_table")
async def get_complete_network_table_route(label: str, query: str = Query(...)):
    try:
        tables = get_complete_network_table.get_complete_network_table(label, query)
        return {"tables": tables}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


