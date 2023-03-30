function readmoreprob(){
    let des_prob= document.getElementById("probdescription").innerHTML;
    let help_prob = document.getElementById("help").innerHTML;
    let prog_prob = document.getElementById("progress").innerHTML;
    let prob_name = document.getElementById("pname").innerHTML;
    document.getElementById("problemname").innerHTML = prob_name+`<br>`+ des_prob +`<br>`+help_prob +`<br>`+prog_prob;
}