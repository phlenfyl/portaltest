window.addEventListener('DOMContentLoaded', function() {
    handleDjangoMessages();
    handleQueryRemoval('orderID');
})

const handleQueryRemoval = (query) => {
    const url = new URL(window.location.href);
    url.searchParams.delete(query); 
    window.history.pushState({}, '', url);
}

const handleDjangoMessages = () => {
    
    document.getElementById('close')?.addEventListener('click', function() {
       const message =  document.getElementById('message')
       if( message){
           message.style.display = 'none';
       }
    });

    
    setTimeout(function() {
        const message = document.getElementById('message')
        if (message){
            message.style.display = 'none';
        }
    }, 6000);
}