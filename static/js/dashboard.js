window.addEventListener("DOMContentLoaded", () => {
    handleCloseDetailModal();
    handleDetailsRequest();
    handleGenerateReportSubmit();
    handleSaveTemplates();
    // handleRoportPageFunctionalty();
    handlePaginationButtons();
    handleClearFilter();
    handleSort();
    handleSearch();
    handleToggleGenerateReportModal();
    handleSearchIDBtn();
    hideDateFilters();
})
const handleSearchIDBtn = () => {
    // disable the search button if the input is empty
    const searchIDBtn = document.getElementById("searchIDBtn")
    const searchIDInput = document.getElementById("searchIDInput")
    searchIDBtn.disabled = true 
    searchIDBtn.classList.add("opacity-[0.6]")
    searchIDInput.addEventListener( "keyup", (e) => {
        if(e.target.value !== ""){
            searchIDBtn.disabled = false 
            searchIDBtn.classList.remove("opacity-[0.6]")
        }else{
            searchIDBtn.disabled = true 
            searchIDBtn.classList.add("opacity-[0.6]")
        }
    })
}

const hideDateFilters = () => {
    // ensures the date filters only work with delivered, statusCodeAdded and attempted dilevery status
    const deliveryStatus = document.getElementById('deliveryStatus');
    const check = deliveryStatus.querySelectorAll('input[type="checkbox"]')
    const endDateInput = document.getElementById('endDate');
    const startDateInput = document.getElementById('startDate');
    const dateContainer = document.querySelectorAll('.filter-dates');
    const filter = document.getElementById("searchBtn")

    check.forEach(function (){
        if (this.checked) {
            console.log(this.value)
            if (this.value === 'delivered' || this.value === 'statusCodeAdded' || this.value === 'attempted' || this.value === 'pickedup') {
                
                endDateInput.disabled = false;
                startDateInput.disabled = false;
                console.log(endDateInput.value, startDateInput.value)
                dateContainer.forEach(function (el) {
                    el.classList.remove('opacity-50');
                })
            };
        }
    })

    filter.addEventListener('click', function() {
        check.forEach(function (){
            if (this.checked) {
                console.log(this.value)
                if (this.value && endDateInput === '' || this.value && startDateInput === '') {
                    filter.disabled = true;
                }else if (this.value && startDateInput === ''){
                    filter.disabled = true;
                }else if (this.value && endDateInput === ''){
                    filter.disabled = true;
                }else{
                    filter.disabled = false;
                }
            }
        });
    })

    deliveryStatus.addEventListener('change', function() {
        check.forEach(function (checkbox) {
          if (checkbox.checked) {
            console.log(checkbox.value)
            if (checkbox.value === 'delivered' || checkbox.value === 'statusCodeAdded' || checkbox.value === 'attempted' || checkbox.value === 'pickedup') {
                
                endDateInput.disabled = false;
                startDateInput.disabled = false;
                console.log(endDateInput.value, startDateInput.value)
                dateContainer.forEach(function (el) {
                    el.classList.remove('opacity-50');
                })
            };
            }
        })
    });


}

const handleSearch = () => {
    // disable the generate button if the the user hasn't searched for anything
    const generateReportBtn = document.getElementById('generate_report');
    const saveTemplateBtn = document.getElementById('saveTemplateBtn');
    
    const url = new URL(window.location.href);
    const params = url.search;
    if (params.includes('deliverystatus') || params.includes('template_id')) {
        generateReportBtn.disabled = false;
        generateReportBtn.classList.remove('opacity-50');
        saveTemplateBtn.disabled = false;
        saveTemplateBtn.classList.remove('opacity-50');
    }

}

const handleSort = () => {
    // This function handles the sorting of the table
    document.getElementById('sort-by-id').addEventListener('click', function(event) {
        event.preventDefault();
        toggleSort('id');
    });
    
    document.getElementById('sort-by-status').addEventListener('click', function(event) {
        event.preventDefault();
        toggleSort('status');
    });
    
    document.getElementById('sort-by-date').addEventListener('click', function(event) {
        event.preventDefault();
        toggleSort('date');
    });
}

function toggleSort(sortKey) {
    let url = new URL(window.location.href);
    if (url.searchParams.get('sort') === sortKey) {
        url.searchParams.delete('sort');
    } else {
        url.searchParams.set('sort', sortKey);
    }
    window.location.href = url;
}

const handleToastMessages = (message, statusClass) => {
    const toast = document.getElementById('toast');
    const close = document.getElementById('close');
    const toastMessage = document.getElementById('toastMessage');
    

    toast.classList.remove('hidden');
    toastMessage.innerHTML = message;
    toast.classList.add('opacity-100');
    toast.classList.add(...statusClass);
    
    
    const interval = setTimeout(function() {
        toast.classList.add('hidden');
        toast.classList.remove(...statusClass);
    }, 8000);

    
    close.onclick = function() {
        toast.classList.add('hidden');
        toast.classList.remove(...statusClass);
        clearTimeout(interval);
    };
}

const handlePaginationButtons = () => {
    const buttons = document.querySelectorAll('a.paginationBtn');
    buttons?.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            const page = href.split('=')[1];
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('page', page);
            window.location.href = currentUrl.toString();
        });
    });
}

const handleCloseDetailModal = () => {
    const closeDetailBtn = document.getElementById('closeDetailBtn');
    closeDetailBtn?.addEventListener('click', () => {
        const detailModal = document.getElementById('sidebar-modal');
        detailModal.classList.add('hidden');
        // get the url and remove the query
        const url = new URL(window.location.href);
        url.searchParams.delete('external_id');
        history.replaceState({}, null, url);
    })
}

const handleDetailsRequest = () => {
    document.querySelectorAll('.add-params').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            var url = new URL(window.location.href);
            url.searchParams.set(this.dataset.paramName, this.dataset.paramValue);
            window.location.href = url.href;
        });
    });
}

// handles generate report submition
const handleGenerateReportSubmit = () => {
    const generateReportForm = document.getElementById("generateReportForm");
    generateReportForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const deliveryStatus = document.getElementById("deliveryStatus");
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        const customerState = document.getElementById("customerState").value;
        const customercity = document.getElementById("customerCity").value;
        const selectReport = document.getElementById("select-report").value;
        const address = document.getElementById("address").value;
        const customername = document.getElementById("customername").value;
        // const subject = document.getElementById("subject").value;
        // const description = document.getElementById("description").value;
        // const addAutomation = document.getElementById("addAutomation").checked;
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        // const radios = document.querySelectorAll('input[type="radio"][name="calendar"]');
        const generateReportBtn = document.getElementById("generate_report_btn");
        const spinner = document.getElementById("generate_report_spinner");
        const generateBtnText = document.getElementById("generate_report_btn_text");

        function getStatusChecked(deliverystatus) {
            const check = deliveryStatus.querySelectorAll('input[type="checkbox"]')
            const checkedValues = []
            for (const checkbox of check) {
                if (checkbox.checked) {
                    checkedValues.push(checkbox.value.replace(/,/g, ' '))
                }
            }
            if(checkedValues.length > 1){
                return checkedValues.join(",");
            }else{
                return checkedValues;
            }
            
        }

        const finalchecks =  getStatusChecked(deliveryStatus)
        console.log(finalchecks)
        // if (finalchecks.length > 1){
        //     const errormsg = document.getElementById("infoalert");
        //     errormsg.classList.remove("hidden");
        //     errormsg.innerHTML = 
        //     `
        //         <p>Please select only one delivery status for report generation.</p>
        //         <svg onclick="return this.parentNode.remove();" class="inline w-3 h-3 fill-current ml-2 hover:opacity-80 cursor-pointer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        //             <path d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 464c-114.7 0-208-93.31-208-208S141.3 48 256 48s208 93.31 208 208S370.7 464 256 464zM359.5 133.7c-10.11-8.578-25.28-7.297-33.83 2.828L256 218.8L186.3 136.5C177.8 126.4 162.6 125.1 152.5 133.7C142.4 142.2 141.1 157.4 149.7 167.5L224.6 256l-74.88 88.5c-8.562 10.11-7.297 25.27 2.828 33.83C157 382.1 162.5 384 167.1 384c6.812 0 13.59-2.891 18.34-8.5L256 293.2l69.67 82.34C330.4 381.1 337.2 384 344 384c5.469 0 10.98-1.859 15.48-5.672c10.12-8.562 11.39-23.72 2.828-33.83L287.4 256l74.88-88.5C370.9 157.4 369.6 142.2 359.5 133.7z"/>
        //         </svg>
        //     `
        //     return;
        // }else{
        //     const errormsg = document.getElementById("infoalert");
        //     errormsg.classList.add("hidden");
        // }


        const data = {
            csrfmiddlewaretoken: csrftoken,
            deliverystatus: finalchecks,
            start_date: startDate,
            end_date: endDate,
            customerstate: customerState,
            customercity: customercity,
            report_type: selectReport,
            customername : customername,
            address : address
            // email: emailList,
            // subject: subject,
            // description: description,
            // addAutomation,
            // schedule: selectedValue
        }

        const formData = new FormData();
        for (var key in data) {
            formData.append(key, data[key])
        }
        console.log(formData)
        const errorClasses = ["bg-red-500", "border-red-700"]
        const successClasses = ["bg-green-500", "border-green-700"]

        spinner.classList.remove("hidden");
        generateBtnText.classList.add("hidden");
        generateReportBtn.disabled = true;

        try {
            const res = await fetch("/dashboard", {
                method: "POST",
                body: formData
            })
            if (!res.ok) {
                const data = await res.json();
                const msg = data.error ? `${data.error.map(e => `<li>${e}</li>`).join('')}` : "Report Generation failed";
                handleToastMessages(msg, errorClasses);
            }else{
                 // Create an object URL for the blob
                blob = await res.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                
                const contentType = res.headers.get('Content-Type');
                // Set the filename based on the file type
                if (contentType === 'text/csv') {
                    a.download = 'orders.csv';
                } else if (contentType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
                    a.download = 'orders.xlsx';
                } else {
                    // Handle other file types if necessary
    }
                
                document.body.appendChild(a);
                a.click();
                
                // clean-up
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                handleToastMessages("Report Generated Succesfully", successClasses);
            }
            
        } catch (error) {
            console.error('An error occurred:', error);
            handleToastMessages("Report Generation failed", errorClasses);
        }
        generateReport();

        generateReportBtn.disabled = false;
        generateBtnText.classList.remove("hidden");
        spinner.classList.add("hidden");

    })



}

const handleClearFilter = () => {
    const clearFilterBtn = document.getElementById("clearFilterBtn");
    clearFilterBtn.addEventListener("click", (e) => {
        const url = new URL(window.location.href);
        url.search = "";
        window.location.href = url.href;
    })

}
// handle saving templates 
const handleSaveTemplates = () => {
    const saveTemplateBtn = document.getElementById("saveTemplateBtn");
    saveTemplateBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        const deliveryStatus = document.getElementById("deliveryStatus");
        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const startDate = document.getElementById("startDate").value;
        const endDate = document.getElementById("endDate").value;
        const customerState = document.getElementById("customerState").value;
        const customercity = document.getElementById("customerCity").value;
        const customername = document.getElementById("customername").value;
        const address = document.getElementById("address").value;

        function getStatusChecked(deliverystatus) {
            const check = deliveryStatus.querySelectorAll('input[type="checkbox"]')
            const checkedValues = []
            for (const checkbox of check) {
                if (checkbox.checked) {
                    checkedValues.push(checkbox.value)
                }
            }  
            
            return checkedValues.join(",");
        }

       const finalchecks =  getStatusChecked(deliveryStatus)
        console.log(finalchecks)

    //    if (finalchecks.length > 1){
    //         const errormsg = document.getElementById("infoalert");
    //         errormsg.classList.remove("hidden");
    //         errormsg.innerHTML = 
    //         `
    //             <p>Only support a single selection to save template</p>
    //             <svg onclick="return this.parentNode.remove();" class="inline w-3 h-3 fill-current ml-2 hover:opacity-80 cursor-pointer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
    //                 <path d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 464c-114.7 0-208-93.31-208-208S141.3 48 256 48s208 93.31 208 208S370.7 464 256 464zM359.5 133.7c-10.11-8.578-25.28-7.297-33.83 2.828L256 218.8L186.3 136.5C177.8 126.4 162.6 125.1 152.5 133.7C142.4 142.2 141.1 157.4 149.7 167.5L224.6 256l-74.88 88.5c-8.562 10.11-7.297 25.27 2.828 33.83C157 382.1 162.5 384 167.1 384c6.812 0 13.59-2.891 18.34-8.5L256 293.2l69.67 82.34C330.4 381.1 337.2 384 344 384c5.469 0 10.98-1.859 15.48-5.672c10.12-8.562 11.39-23.72 2.828-33.83L287.4 256l74.88-88.5C370.9 157.4 369.6 142.2 359.5 133.7z"/>
    //             </svg>
    //         `
    //         return;
    //     }else{
    //         const errormsg = document.getElementById("infoalert");
    //         errormsg.classList.add("hidden");
    //     }
        
        const data = {
            csrfmiddlewaretoken: csrftoken,
            deliverystatus: finalchecks,
            start_date: startDate,
            end_date: endDate,
            customerstate: customerState,
            customercity: customercity,
            customername: customername,
            address: address,
        }

        const formData = new FormData();
        for (var key in data) {
            formData.append(key, data[key])
        }
        // code that displays a loeding spinner until the request is complete
        const spinner = document.getElementById("spinner");
        const confirmTick = document.getElementById("confirmTick");
        const errorClasses = ["bg-red-500", "border-red-700"]
        const successClasses = ["bg-green-500", "border-green-700"]
        spinner.classList.toggle("hidden");
        saveBtnText.classList.toggle("hidden");
        saveTemplateBtn.disabled = true;

        try {
            const res = await fetch("/add-template/", {
                method: "POST",
                body: formData,
            })
            if (!res.ok) {
                const error = await res.json();
                handleToastMessages("Must have atleast one filter", errorClasses);
                saveBtnText.classList.remove("hidden");

            } else {
                confirmTick.classList.remove("hidden");
                handleToastMessages("Filters saved to templates", successClasses);
                setTimeout(() => {
                    confirmTick.classList.add("hidden");
                    saveBtnText.classList.toggle("hidden");
                }, 3000)
            }
        } catch (error) {
            console.error('An error occurred:', error);
            handleToastMessages("an error occured while saving the template", errorClasses);
            saveBtnText.classList.remove("hidden");
        }
        spinner.classList.toggle("hidden");
        saveTemplateBtn.disabled = false;


    })
}

const handleSaveTemplateErrors = (text = "", messages) => {
    const saveBtnText = document.getElementById("saveBtnText");
    saveBtnText.classList.remove("hidden");

    // iterate through the error message and save it to the error container
    templateErrorContainer.classList.remove("hidden");
    if (text) {
        templateErrorContainer.innerHTML += `<li>${text}</li>`
    } else {
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
            return radios[i].value;
        }
    }
}

const handleToggleGenerateReportModal = () => {
    const generateReportBtn = document.getElementById("generate_report");
    generateReportBtn.addEventListener("click", (e) => {
        e.preventDefault();
    //     const deliveryStatus = document.getElementById("deliveryStatus");

    //     function getStatusChecked(deliverystatus) {
    //         const check = deliveryStatus.querySelectorAll('input[type="checkbox"]')
    //         const checkedValues = []
    //         for (const checkbox of check) {
    //             if (checkbox.checked) {
    //                 checkedValues.push(checkbox.value)
    //             }
    //         }  
            
    //         return checkedValues;
    //     }

    //     const finalchecks =  getStatusChecked(deliveryStatus)

    //    if (finalchecks.length > 1){
    //         const errormsg = document.getElementById("infoalert");
    //         errormsg.classList.remove("hidden");
    //         errormsg.innerHTML = 
    //         `
    //             <p>Only support one status selection to generate report</p>
    //             <svg onclick="return this.parentNode.remove();" class="inline w-3 h-3 fill-current ml-2 hover:opacity-80 cursor-pointer" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
    //                 <path d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 464c-114.7 0-208-93.31-208-208S141.3 48 256 48s208 93.31 208 208S370.7 464 256 464zM359.5 133.7c-10.11-8.578-25.28-7.297-33.83 2.828L256 218.8L186.3 136.5C177.8 126.4 162.6 125.1 152.5 133.7C142.4 142.2 141.1 157.4 149.7 167.5L224.6 256l-74.88 88.5c-8.562 10.11-7.297 25.27 2.828 33.83C157 382.1 162.5 384 167.1 384c6.812 0 13.59-2.891 18.34-8.5L256 293.2l69.67 82.34C330.4 381.1 337.2 384 344 384c5.469 0 10.98-1.859 15.48-5.672c10.12-8.562 11.39-23.72 2.828-33.83L287.4 256l74.88-88.5C370.9 157.4 369.6 142.2 359.5 133.7z"/>
    //             </svg>
    //         `
    //         return;
    //     }else{
    //         const errormsg = document.getElementById("infoalert");
    //         errormsg.classList.add("hidden");
    //     }
        generateReport()
    });
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