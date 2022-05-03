// npm install prompt-sync
// node app.js
// const input = require('sync-input'); // for jetbrains
const input = require('prompt-sync')(); // for node
const welcome_msg =`Welcome to Currency Converter!
1 USD equals  1 USD
1 USD equals  113.5 JPY
1 USD equals  0.89 EUR
1 USD equals  74.36 RUB
1 USD equals  0.75 GBP`;
const what_msg = `What do you want to do?
1-Convert currencies 2-Exit program`

currencies = {"usd":1, "gbp":0.75, "jpy":113.5, "eur":0.89, "rub":74.36}

calculate = function (amount, from, to) {
	value = (amount * currencies[to] / currencies[from]).toFixed(4);
	return value;
}

read_amount = function () {
	amount = input("Amount: ");
	if (isNaN(amount)) {
		console.log("The amount has to be a number");
	} else if (amount < 1) {
		console.log("The amount can not be less than 1")
	}
	else {
		return amount
	}
}

readInput = function (text) {
	entered = input(text).toLowerCase()
	if (currencies[entered] == undefined) {
		console.log("Unknown currency");
	}
	else {
		return entered
	}
}

console.log(welcome_msg)

while (true) {
	console.log(what_msg)
	entered = input()
	if (entered == 2) {
		console.log("Have a nice day!");
		break;
	} else if (entered != 1) {
		console.log("Unknown input")
		continue;
	}
	console.log("What do you want to convert?")
	from = readInput("From: ");
	if (!from) {
		continue;
	}
	to = readInput("To: ");
	if (!to) {
		continue;
	}
	amount = read_amount();
	if (!amount) {
		continue;
	}
	result = calculate(amount, from, to);
	console.log(`Result: ${amount} ${from.toUpperCase()} equals ${result} ${to.toUpperCase()}`);
}