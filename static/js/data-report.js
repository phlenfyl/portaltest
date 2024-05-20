window.addEventListener("DOMContentLoaded", () => {
    handleGenerateReportSubmit();
    handleSaveTemplates();
    handleRoportPageFunctionalty();
})

// handles generate report submition
const handleGenerateReportSubmit = () => {
    const generateReportForm = document.getElementById("generateReportForm");
    generateReportForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const deliveryStatus = document.getElementById("deliveryStatus").value;
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        const customerState = document.getElementById("customerState").value;
        const customercity = document.getElementById("customerCity").value;
        const selectReport = document.getElementById("select-report").value;
        const subject = document.getElementById("subject").value;
        const description = document.getElementById("description").value;
        const addAutomation = document.getElementById("addAutomation").checked;
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const radios = document.querySelectorAll('input[type="radio"][name="calendar"]');
        const generateReportBtn = document.getElementById("generate_report_btn");
        const spinner = document.getElementById("generate_report_spinner");
        const generateBtnText = document.getElementById("generate_report_btn_text");

        let selectedValue = "None"
        if (addAutomation) {
            selectedValue = getSelectedValue(radios);
        }
        
        const data = {
            csrfmiddlewaretoken: csrftoken,
            deliverystatus: deliveryStatus,
            start_date: startDate,
            end_date: endDate,
            customerstate: customerState,
            customercity: customercity,
            report_type: selectReport,
            email: emailList,
            subject: subject,
            description: description,
            addAutomation,
            schedule: selectedValue
        }
        
        const formData = new FormData();
        for (var key in data) {
            formData.append(key, data[key])
        }
        spinner.classList.remove("hidden");
        generateBtnText.classList.add("hidden");
        generateReportBtn.disabled = true;

        try {
            const res = await fetch("/data-report/", {
                method: "POST",
                body: formData
            })
            if (!res.ok) {
                console.log(`HTTP error! status: ${response.status}`)
            }
            
            // location.reload()
        } catch (error) {
            console.error('An error occurred:', error);
        }

        generateReportBtn.disabled = false;
        generateBtnText.classList.remove("hidden");
        spinner.classList.add("hidden");

    })



}

// handle saving templates 
const handleSaveTemplates = () => {
    const saveTemplateBtn = document.getElementById("saveTemplateBtn");
    saveTemplateBtn.addEventListener('click', async () => {
        const deliveryStatus = document.getElementById("deliveryStatus").value;
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        const customerState = document.getElementById("customerState").value;
        const customercity = document.getElementById("customerCity").value;
        const templateErrorContainer = document.getElementById("templateErrorContainer");
        const data = {
            csrfmiddlewaretoken: csrftoken,
            deliverystatus: deliveryStatus,
            start_date: startDate,
            end_date: endDate,
            customerstate: customerState,
            customercity: customercity,
        }
        
        const formData = new FormData();
        for (var key in data) {
            formData.append(key, data[key])
        }
        // code that displays a loeding spinner until the request is complete
        const spinner = document.getElementById("spinner");
        const confirmTick = document.getElementById("confirmTick");
        spinner.classList.remove("hidden");
        saveBtnText.classList.add("hidden");
        saveTemplateBtn.disabled = true;

        try {
            const res = await fetch("/add-template/", {
                method: "POST",
                body: formData,
            })
            console.log(res)
            if (!res.ok) {
                const error = await res.json();
                handleSaveTemplateErrors(text = null, error.message)
            }else{
                confirmTick.classList.remove("hidden");
                setTimeout(() => {
                    confirmTick.classList.add("hidden");
                    saveBtnText.classList.remove("hidden");
                }, 3000)
            }
        } catch (error) {
            console.error('An error occurred:', error);
            handleSaveTemplateErrors("an error occured while saving the template")
            saveBtnText.classList.remove("hidden");
        }
        saveTemplateBtn.disabled = false;
        spinner.classList.add("hidden");
        
    })
}

const handleSaveTemplateErrors = (text = "", messages) => {    
    const saveBtnText = document.getElementById("saveBtnText");
    saveBtnText.classList.remove("hidden");

    // iterate through the error message and save it to the error container
    templateErrorContainer.classList.remove("hidden");
    if(text){
        templateErrorContainer.innerHTML += `<li>${text}</li>`
    }else{
        for (let key in messages) {
            messages[key].forEach((err) => {
                templateErrorContainer.innerHTML += `<li>${err}</li>`
            })
        }
    }
    // add a timeout to remove the error message after 5 seconds
    setTimeout(() => {
        templateErrorContainer.classList.add("hidden");
        templateErrorContainer.innerHTML = "";
    }, 5000)
}
// Function to get the value of the selected radio button
function getSelectedValue(radios) {
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            console.log(radios[i].value)
            return radios[i].value;
        }
    }
}


const handleRoportPageFunctionalty = () => {
    let checkboxReport = document.getElementById("checkbox_thead_report")

    checkboxReport?.addEventListener("change", () => {
        var checkboxes = document.getElementsByTagName("input")

        for (var i = 0; i < checkboxes.length; i++) {
            checkboxes[i].checked = checkboxReport.checked
        }
    })

    //   modal dialog form

    const selectReport = document.getElementById("select-report")
    const emailbox = document.getElementById("emailbox")
    const subjectReport = document.getElementById("subject")
    const description = document.getElementById("description")
    const generateReportBtn = document.getElementById("generate_report_btn")
    const checkboxAddAutomation = document.getElementById("addAutomation")
    const calendars = document.getElementById("calendars")

    function checkInputs() {
        if (
            emailbox.value.trim() === "" &&
            selectReport.value.trim() === "" &&
            subjectReport.value.trim() === "" &&
            description.value.trim() === "" &&
            checkboxAddAutomation.checked !== true
        ) {
            generateReportBtn.disabled = true
        } else {
            generateReportBtn.disabled = false
        }

        if (checkboxAddAutomation.checked) {
            calendars.style.display = "flex"
        } else {
            calendars.style.display = "none"
        }
    }

    checkInputs()
    emailbox.addEventListener("change", transformEmails)
    selectReport.addEventListener("change", checkInputs)
    emailbox.addEventListener("input", checkInputs)
    subjectReport.addEventListener("input", checkInputs)
    description.addEventListener("input", checkInputs)
    checkboxAddAutomation.addEventListener("change", checkInputs)
}

function generateReport() {
    const modal = document.getElementById("modal-generate")

    if (modal) {
        modal.classList.toggle("open")
    }
}

function closeModal() {
    const modal = document.getElementById("modal-generate")

    if (modal) {
        modal.classList.remove("open")
    }
}

function closeSidebarReport() {
    location.href = "/data-report/"
}

var emailList

function transformEmails() {
    if (emailbox.value.includes(",")) {
        const emailbox = document.getElementById("emailbox")
        emailList = emailbox.value.split(",")
        console.log({ emailList })
        const emailListBox = document.getElementById("emailList")
        emailList.forEach((email, idx) => {
            emailListBox.innerHTML += `
                <span class="px-2 py-1 rounded-md border border-neutral-100 text-sm font-medium flex items-center gap-1"
                                >
                                  <span class="">${email.trim()}</span>
                                  <div class="w-3 h-3 cursor-pointer" onclick="removeEmail(${idx})">
                                    <img
                                      src="/assets/images/xclose.svg"
                                      alt=""
                                      class="w-full h-full object-contain"
                                    />
                                  </div>
                                </span>
                `
        })
        emailbox.value = ""
    }
}

function removeEmail(index) {
    if (index >= 0 && index < emailList.length) {
        emailList.splice(index, 1)
        updateEmailList()
    }
}

function updateEmailList() {
    const emailListBox = document.getElementById("emailList")
    emailListBox.innerHTML = ""

    if (emailList.length > 0) {
        emailList.forEach((email, idx) => {
            emailListBox.innerHTML += `
            <span class="px-2 py-1 rounded-md border border-neutral-100 text-sm font-medium flex items-center gap-1"
                            >
                              <span class="">${email.trim()}</span>
                              <div class="w-3 h-3 cursor-pointer" onclick="removeEmail(${idx})">
                                <img
                                  src="/assets/images/xclose.svg"
                                  alt=""
                                  class="w-full h-full object-contain"
                                />
                              </div>
                            </span>
            `
        })
    }
}
