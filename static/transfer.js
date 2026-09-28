let btn= document.getElementById("find")
console.log(btn)
btn.onclick= e=>{
    let acc1=document.getelementById("from").value
    console.log("Entered account:",acc1)
    if(acc1 ==""){
        alert("please enter account number");
        return;
    }
    fetch('holder_acc',{
        method:"POST",
        body:JSON.stringify({
            accountnumber:acc1
        })
    })
    .then(res =>{
        console.log("Response status:",res.status);
        return res.json();
    })
    .then(data =>{
        console.log(data);
        if (data.success){
            document.getElementById("Holder_name").innerText=
            "Account Holder:" +data.username;
        }
        else{
            document.getElementById("Holder_name").innerText=
            "Account not found";
        }
    })
    .catch(error =>console.log("Error",error))
}