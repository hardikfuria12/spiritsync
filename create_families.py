from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)
# Load Excel data
excel_path = "transformed_flr_01-Apr-2025.xlsx"
df = pd.read_excel(excel_path)

# Select only relevant columns
rows = df[['brand', 'size', 'scmcode']].to_dict(orient='records')

# HTML template with embedded JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <title>SCM Code Family Grouper</title>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
    th, td { border: 1px solid #ddd; padding: 8px; }
    th { background-color: #f4f4f4; }
    .family-display { margin-top: 30px; }
    .family-block { margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; }
  </style>
</head>
<body>

<h2>SCM Code Family Grouper</h2>

<label for="familyName">Enter Family Name:</label>
<input type="text" id="familyName" placeholder="e.g. Family_A">
<button onclick="groupSelected()">Group into Family</button>

<table id="scmTable">
  <thead>
    <tr>
      <th>Select</th>
      <th>Brand</th>
      <th>Size</th>
      <th>SCM Code</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>

<div class="family-display" id="familyDisplay">
  <h3>Grouped Families:</h3>
</div>

<script>
  const data = {{ rows | tojson }};

  const tbody = document.querySelector("#scmTable tbody");
  const familyDisplay = document.getElementById("familyDisplay");

  function renderTable() {
    tbody.innerHTML = '';
    data.forEach((item, index) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td><input type="checkbox" data-index="${index}"></td>
        <td>${item.brand}</td>
        <td>${item.size}</td>
        <td>${item.scmcode}</td>
      `;
      tbody.appendChild(row);
    });
  }

  function groupSelected() {
    const checkboxes = document.querySelectorAll("input[type=checkbox]:checked");
    const familyName = document.getElementById("familyName").value.trim();

    if (!familyName) {
      alert("Please enter a family name.");
      return;
    }

    if (checkboxes.length < 2) {
      alert("Please select at least two SCM codes to group.");
      return;
    }

    const familyBlock = document.createElement("div");
    familyBlock.className = "family-block";
    familyBlock.innerHTML = `<strong>${familyName}</strong>: `;

    const indexesToRemove = [];

    checkboxes.forEach(cb => {
      const index = parseInt(cb.getAttribute("data-index"));
      const item = data[index];
      familyBlock.innerHTML += `${item.scmcode} &nbsp; `;
      indexesToRemove.push(index);
    });

    indexesToRemove.sort((a, b) => b - a).forEach(i => data.splice(i, 1));

    familyDisplay.appendChild(familyBlock);
    renderTable();
    document.getElementById("familyName").value = '';
  }

  renderTable();
</script>

</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
