$(document).ready(function (){

    function basketUpdating(product_id, count, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.count = count;
        var csrf_token = $('#get-csrf-token [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data['is_delete'] = true;
        }

        var url = form.attr('action');
        console.log(data);
        $.ajax({
            url: '/basket_adding',
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log('OK');
                console.log(data.products_total_count)
                if (data.products_total_count || data.products_total_count == 0) {
                    $('#basket-total-count').text(" (" + data.products_total_count + ")");
                    console.log(data.products);
                }
            location.reload();
            },
            error: function () {
                console.log('error');
            }
        })
    }

    function basketEditing(product_id, count) {
        var data = {};
        data.id = product_id;
        data.count = count;
        var csrf_token = $('#get-csrf-token [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            url: '/basket_editing',
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log('OK');
            },
            error: function () {
                console.log('error');
            }
        })
    }

    var form = $('#form_buying_product')
    console.log(form);
    form.on('submit', function (e){
        e.preventDefault();
        var count = $('#number').val();
        console.log(count);
        var submit_btn = $('#submit-btn');
        var product_id = submit_btn.data("product_id");
        var product_name = submit_btn.data("product_name")
        var product_price = submit_btn.data(("product_price"))

        basketUpdating(product_id, count, is_delete=false)
    });

    $(document).on('click', '.delete-item', function (e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        count = 0;
        basketUpdating(product_id, count, is_delete=true)
    });

    function calculatingBasketAmount(){
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function(){
            total_order_amount += parseFloat($(this).text());
        });
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', '.product-in-basket-count', function (){
        var current_count = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        var total_amount = parseFloat(current_count * current_price).toFixed(2);
        current_tr.find('.total-product-in-basket-amount').text(total_amount + ' KZT');
        calculatingBasketAmount();

        var btn = current_tr.find('.delete-item')
        id = btn.data('product_id')
        basketEditing(id, current_count)
    });

    calculatingBasketAmount();

});