// ----------------------------------------
// PDF UPLOAD
// ----------------------------------------

const uploadForm = document.getElementById("uploadForm");

uploadForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const fileInput = document.getElementById("pdfFile");
    const uploadStatus = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        uploadStatus.innerHTML = `
            <div class="alert alert-warning">
                Please select a PDF file.
            </div>
        `;
        return;
    }

    const file = fileInput.files[0];

    // Make sure it is a PDF
    if (file.type !== "application/pdf") {
        uploadStatus.innerHTML = `
            <div class="alert alert-danger">
                Please select a PDF file.
            </div>
        `;
        return;
    }

    const formData = new FormData();

    formData.append("pdf", file);

    uploadStatus.innerHTML = `
        <div class="alert alert-info">
            Processing PDF... Please wait.
        </div>
    `;

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed.");
        }

        uploadStatus.innerHTML = `
            <div class="alert alert-success">
                <strong>PDF uploaded successfully!</strong><br>
                File: ${data.filename}<br>
                Pages: ${data.pages}<br>
                Chunks: ${data.chunks}
            </div>
        `;

    } catch (error) {

        uploadStatus.innerHTML = `
            <div class="alert alert-danger">
                ${error.message}
            </div>
        `;
    }

});


// ----------------------------------------
// ASK QUESTION
// ----------------------------------------

const askButton = document.getElementById("askButton");

askButton.addEventListener("click", async function () {

    const questionInput = document.getElementById("questionInput");

    const question = questionInput.value.trim();

    const loading = document.getElementById("loading");

    const answerSection = document.getElementById("answerSection");

    const answer = document.getElementById("answer");

    const sources = document.getElementById("sources");


    // Check question
    if (!question) {

        alert("Please enter a question.");

        return;
    }


    // Show loading
    loading.classList.remove("d-none");

    answerSection.classList.add("d-none");

    askButton.disabled = true;


    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Something went wrong."
            );

        }


        // Display answer
       answer.innerHTML = marked.parse(data.answer);


        // Display sources
        sources.innerHTML = "";

        const uniqueSources = [...new Set(data.sources)];

        uniqueSources.forEach(function (page) {

            const badge = document.createElement("span");

            badge.className = "badge bg-secondary me-2";

            badge.textContent = `Page ${page}`;

            sources.appendChild(badge);

        });


        answerSection.classList.remove("d-none");


    } catch (error) {

        answer.textContent = error.message;

        answerSection.classList.remove("d-none");

    } finally {

        loading.classList.add("d-none");

        askButton.disabled = false;

    }

});


// ----------------------------------------
// PRESS ENTER TO ASK
// ----------------------------------------

document
    .getElementById("questionInput")
    .addEventListener("keydown", function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            askButton.click();

        }

    });


// ----------------------------------------
// CLEAR PDF
// ----------------------------------------

const clearButton = document.getElementById("clearButton");

clearButton.addEventListener("click", async function () {

    try {

        const response = await fetch("/clear", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.error || "Could not clear PDF."
            );
        }

        // Clear selected file
        document.getElementById("pdfFile").value = "";

        // Clear upload status
        document.getElementById("uploadStatus").innerHTML = `
            <div class="alert alert-info">
                PDF cleared successfully. You can upload another PDF.
            </div>
        `;

        // Clear question
        document.getElementById("questionInput").value = "";

        // Hide previous answer
        document
            .getElementById("answerSection")
            .classList.add("d-none");

    } catch (error) {

        document.getElementById("uploadStatus").innerHTML = `
            <div class="alert alert-danger">
                ${error.message}
            </div>
        `;

    }

});
