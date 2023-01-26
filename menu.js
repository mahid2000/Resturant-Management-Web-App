// JavaScript code to fetch menu items from a JSON file
// JavaScript code to add a dish to the menu
document.getElementById("add-dish-button").addEventListener("click", function(event) {
  event.preventDefault();

  let dishName = document.getElementById("dish-name").value;
  let dishDescription = document.getElementById("dish-description").value;
  let dishPrice = document.getElementById("dish-price").value;
  let dishImage = document.getElementById("dish-image").files[0];

  let dish = {
    name: dishName,
    description: dishDescription,
    price: dishPrice,
    image: dishImage
  };
  // code to save the dish to a database or json file here
  let menuItems = document.getElementById("menu-items");
  let dishNode = document.createElement("div");
  dishNode.classList.add("menu-item");
  dishNode.innerHTML = "<img src='" + dish.image + "' alt='" + dish.name + "'>" +
    "<h3>" + dish.name + "</h3>" +
    "<p>" + dish.description + "</p>" +
    "<p>$" + dish.price + "</p>";
  menuItems.appendChild(dishNode);
});
