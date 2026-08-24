// Newsletter form — submits to Formspree without leaving the page.
(function(){
  var form = document.getElementById('newsletter-form');
  if(!form) return;
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var data = new FormData(form);
    fetch(form.action, {
      method: 'POST',
      body: data,
      headers: { 'Accept': 'application/json' }
    }).then(function(res){
      if(res.ok){
        form.classList.add('submitted');
      } else {
        alert('Something went wrong — please try again.');
      }
    }).catch(function(){
      alert('Something went wrong — please check your connection and try again.');
    });
  });
})();
