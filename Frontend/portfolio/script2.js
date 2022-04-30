// https://www.youtube.com/watch?v=gXkqy0b4M5g

const navSlide = function () {
    const burger = document.querySelector(".hamburger");
    const nav = document.querySelector(".links");
    const navLinks = document.querySelectorAll(".links li");
    //togle nav
    burger.addEventListener("click", function (){
        nav.classList.toggle("links-active");
    })
    //animate links
    navLinks.forEach(function (link, index){
        link.style.animation = `navLinkFade 0.5s ease forwards ${index / 5}s`;
        console.log(index / 5 + 0.2);
    })

}

navSlide();
