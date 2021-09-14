naqt_basic_front = """
<h1>NAQT You Gotta Know</h1>

<div class='qcard'>
{{#Category}}<h2>{{Category}}</h2><br/>{{/Category}}

{{Prompt}}

<br/><br/>

<span class="answer-hidden">{{Answer}}</span>
</div>
<div class="source">
<span class="label">Source:</span> <span class="content">{{Source}}</span>
</div>
"""

naqt_basic_back = """
<h1>NAQT You Gotta Know</h1>

<div class='qcard'>
{{#Category}}<h2>{{Category}}</h2><br/>{{/Category}}

{{Prompt}}

<br/><br/>

<span class="answer">{{Answer}}</span>
</div>
<div class="source">
<span class="label">Source:</span> <span class="content">{{Source}}</span>
</div>

{{#Extra}}
<br/>
<div class="extra">
{{Extra}}
</div>
{{/Extra}}
"""

naqt_basic_css = """
body {
background-color: #cceeee;
}

h1 {
text-align: center;
}

.card {
  font-family: arial;
  font-size: 20px;
  color: black;
}

.qcard {
width: 80%;
margin: 4px auto;
background-color: white;
border: 1px solid black;
border-radius: 4px;
padding: 4px 8px;
}

.qcard h2 {
font-size: 130%;
margin: 0;
color: darkblue;
}

.qcard .answer {
color: maroon;
}

.qcard .answer-hidden {
visibility: hidden;
}

.source {
width: 80%;
margin: 4px auto;
font-size: 70%;
text-align: right;
padding: 0 4px;
}

.source .label {
font-weight: bold;
}

.source .content {
font-family: monospace;
font-size: 90%;
}

.extra {
width: 80%;
margin: 4px auto;
}
"""

naqt_cloze_front = """
<h1>NAQT You Gotta Know</h1>

<div class='qcard'>
{{#Category}}<h2>{{Category}}</h2><br/>{{/Category}}

{{cloze:Text}}

</div>
<div class="source">
<span class="label">Source:</span> <span class="content">{{Source}}</span>
</div>
"""

naqt_cloze_back = """
<h1>NAQT You Gotta Know</h1>

<div class='qcard'>
{{#Category}}<h2>{{Category}}</h2><br/>{{/Category}}

{{cloze:Text}}

</div>
<div class="source">
<span class="label">Source:</span> <span class="content">{{Source}}</span>
</div>
"""

naqt_cloze_css = """
body {
background-color: #cceeee;
}

h1 {
text-align: center;
}

.card {
  font-family: arial;
  font-size: 20px;
  color: black;
}

.qcard {
width: 80%;
margin: 4px auto;
background-color: white;
border: 1px solid black;
border-radius: 4px;
padding: 4px 8px;
}

.qcard h2 {
font-size: 130%;
margin: 0;
color: darkblue;
}

.qcard .cloze {
 font-weight: bold;
 color: blue;
}

.source {
width: 80%;
margin: 4px auto;
font-size: 70%;
text-align: right;
padding: 0 4px;
}

.source .label {
font-weight: bold;
}

.source .content {
font-family: monospace;
font-size: 90%;
}

.extra {
width: 80%;
margin: 4px auto;
}
"""

naqt_basic_model_params = {
    "modelName": "NAQT Basic",
    "inOrderFields": ["Prompt", "Answer", "Category", "Source", "Extra"],
     "css": naqt_basic_css,
    "isCloze": False,
    "cardTemplates": [
        {
            "Name": "Card 1",
            "Front": naqt_basic_front,
            "Back": naqt_basic_back
        }
    ]
}

naqt_cloze_model_params = {
    "modelName": "NAQT Cloze",
    "inOrderFields": ["Text", "Category", "Source", "Extra"],
    "css": naqt_cloze_css,
    "isCloze": True,
    "cardTemplates": [
        {
            "Name": "Card 1",
            "Front": naqt_cloze_front,
            "Back": naqt_cloze_back
        }
    ]
}