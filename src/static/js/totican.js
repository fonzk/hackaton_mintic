const buttons = document.querySelectorAll("button");
console.log(buttons);
const button = document.getElementById("in");
button.addEventListener("click",()=>{
    if(buttons[0]["innerText"]=="inicio"){
        buttons[0]["innerText"]="nosotros";
    }else{
        buttons[0]["innerText"]="inicio" 
    }
    
    
    
})

// buttons.addEventListener("click",()=>{
    
//     buttons.classList.toggle("btn-danger");
//     buttons.classList.toggle("btn-primary");
// })
// buttons.forEach(btn=>{
//     btn.addEventListener("click",()=>{
    
//         btn.classList.toggle("disabled");
//     })
// })


console.log(button);
