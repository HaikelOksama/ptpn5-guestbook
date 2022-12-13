
const deleteBtn = document.querySelectorAll('#deleteBtn')
const form = document.getElementById('deleteForm')

function myFunction() {
    let text = "Press a button!\nEither OK or Cancel.";
    if (confirm(text) == true) {
      text = "You pressed OK!";
    } else {
      text = "You canceled!";
    }
  }

  



