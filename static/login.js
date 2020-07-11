function showForm(choice) {
  var joinForm = document.getElementById("joinGame");
  var createForm = document.getElementById("createGame");
  var choiceButtons = document.getElementById("firstChoice");

  choiceButtons.style.display = choiceButtons.style.display == "none" ? "block" : "none";

  switch(choice) {
    case "create":
      createForm.style.display = createForm.style.display == "none" ? "block" : "block";
      break;
    case "join":
      joinForm.style.display = joinForm.style.display == "none" ? "block" : "block"; 
      break;
    }
  }