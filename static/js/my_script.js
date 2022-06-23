(function ($) {
    $(function () {

        //initialize all objects
        $('.modal').modal();
        $('.tabs').tabs();

        // //now you can open modal from code
        // $('#modal1').modal('open');

        //or by click on trigger
        $('.trigger-modal').modal();

        //Barre de côté
        $('.sidenav').sidenav();

    }); // end of document ready
})(jQuery); // end of jQuery name space