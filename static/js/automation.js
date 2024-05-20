window.addEventListener("DOMContentLoaded", () => {
  handleToggleAutomate();
})



const handleToggleAutomate = () => {
  console.log(document.querySelectorAll(".switchbox"))
  document.querySelectorAll(".switchbox").forEach(function (element) {
    element.addEventListener('click', function (event) {
      event.preventDefault();  
      const id = this.getAttribute('data-id'); 
      
      
      fetch(`/toggle-automate/${id}`)
        .then(res => {
          if (!res.ok) {
            this.classList.remove("active")
          }
          return res.json();
        })
        .then(data => {
          this.classList.toggle("active")
        })
        .catch(error => console.error('Error:', error));
      
    });

  })
}