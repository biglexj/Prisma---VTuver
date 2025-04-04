$project = Read-Host "Por favor ingresa el nombre del proyecto"

// Create directories for HTML, CSS, and JavaScript
New-Item -ItemType Directory -Path "$project\assets\css","$project\assets\js","$project\assets\images","$project\docs" -Force
// ... existing code ...
New-Item -ItemType File -Path "$project\index.html","$project\assets\css\style.css","$project\assets\js\script.js","$project\README.md","$project\.gitignore" -Force
// ... existing code ...
Write-Host "✅ Estructura de '$project' creada con éxito."