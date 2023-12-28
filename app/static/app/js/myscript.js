$('#slider1, #slider2, #slider3').owlCarousel({
    loop:true,
    margin:10,
    nav:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },
        1000:{
            items:5
        }
      }
   })

$('.plus-cart').click(function (e) {
    e.preventDefault();
    var id = $(this).attr('pid').toString(); 
    var elm = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type:'GET',
        url:"/pluscart",
        data:{
            prod_id: id
        },
        success: function (data){
            elm.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.total_amount

        }

    })
})

$('.minus-cart').click(function (e) {
    e.preventDefault();
    var id = $(this).attr('pid').toString(); 
    var elm = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type:'GET',
        url:"/minuscart",
        data:{
            prod_id: id
        },
        success: function (data){
            elm.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.total_amount

        }

    })
})

$('.remove-cart').click(function (e) {
    e.preventDefault();
    var id = $(this).attr('pid').toString(); 
    var elm = this
    $.ajax({
        type:'GET',
        url:"/removecart",
        data:{
            prod_id: id
        },
        success: function (data){
            
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.total_amount
            document.getElementById("total_icon").innerText = data.totalitem
            elm.parentNode.parentNode.parentNode.parentNode.remove()  

        }

    })
})
