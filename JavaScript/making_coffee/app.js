// npm install prompt-sync
// node app.js
// const input = require('sync-input');
const input = require('prompt-sync')();

menu = `Write action (buy, fill, take):`

ask_cups = `Write how many cups of coffee you will need:`
money = 550
inventory = {
   "water": 400,
   "milk": 540,
   "coffee beans": 120,
   "disposable cups": 9
}
units = {
   "water": "ml",
   "milk": "ml",
   "coffee beans": "g",
   "disposable cups": "piece"
}

ingredients = {
   "water": 200,
   "milk": 50,
   "coffee beans": 15,
   "disposable cups": 1,
   "money": 5
}

print_coffee_machine = function () {
   console.log(`The coffee machine has:`)
   for (const [key, value] of Object.entries(inventory)) {
      if (key != "disposable cups") {
      console.log(`${value} ${units[key]} of ${key}`);
      } else {
         console.log(`${value} ${key}`)
      }
    }
    console.log(`${money} Dollars`)
    console.log()
}

// fill = function () {
//    ingredients.forEach(element => {
//       console.log(`Write how many ${element[1]} of ${element[2]} you want to add:`)
//       user_input = input()
//       inventory[element[2]] = parseInt(user_input) + inventory[element[2]]
//    })
// }

fill = function () {
   for (const [key, value] of Object.entries(inventory)) {
      console.log(`Write how many ${[units[key]]} of ${key} you want to add:`)
      user_input = parseInt(input())
      inventory[key] = inventory[key] + user_input
    }
}


consume = function (cups) {
   for (const [key, value] of Object.entries(inventory)) {
      inventory[key] = value - ingredients[key] * cups
    }
   money = money + ingredients["money"] * cups
}


check_for_material = function (cups) {
   cups_for_mats = []

   for (const [key, value] of Object.entries(inventory)) {
      available = Math.floor(value / ingredients[key])
      cups_for_mats.push(available)
    }

   can_make = Math.min(...cups_for_mats)
   if (can_make < cups) {
      consume(can_make)
      return `No, I can make only ${can_make} cups of coffee`
   } else if (can_make === cups) {
      consume(can_make)
      return `Yes, I can make that amount of coffee`
   } else {
      consume(can_make)
      return `Yes, I can make that amount of coffee (and even ${can_make - cups} more than that)`
   }
   
}

take_money = function () {
   result = `I gave you \$${money}`
   money = 0
   return result
}

print_coffee_machine()
console.log(menu)
user_input = input()

if (user_input == "take") {
   console.log(take_money())
} else if (user_input == "fill") {
   fill()
} else if(user_input == "buy") {
   console.log(`How many cup of coffe do you want?`)
   user_input = parseInt(input())
   result = check_for_material(user_input)
   console.log(result)
}

print_coffee_machine()