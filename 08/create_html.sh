#!/bin/bash
cat << 'INNER_EOF' > /home/juan/Documents/42/OutCore/piscine_django/django_practice/08/d09/account/templates/account/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account</title>
    <!-- Use Bootstrap according to allowed parameters -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Use JQuery strictly as said in 'Today's specific rules' -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6 text-center">
                
                <!-- Not Connected View -->
                <div id="unauth-view" class="card shadow-sm" style="{% if user.is_authenticated %}display: none;{% endif %}">
                    <div class="card-header bg-dark text-white">
                        <h4 class="mb-0">Connection Form</h4>
                    </div>
                    <div class="card-body">
                        <!-- AJAX Error messages container -->
                        <div id="login-errors" class="alert alert-danger" style="display: none;"></div>
                        
                        <form id="login-form">
                            {% csrf_token %}
                            {{ form.as_p }}
                            <button type="submit" class="btn btn-primary w-100">Log In</button>
                        </form>
                    </div>
                </div>

                <!-- Connected View -->
                <div id="auth-view" class="card shadow-sm" style="{% if not user.is_authenticated %}display: none;{% endif %}">
                    <div class="card-body py-5">
                        <h3 class="mb-4">Logged as <span id="username-display" class="fw-bold text-primary">{{ user.username }}</span></h3>
                        <form id="logout-form">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-danger px-5">Logout</button>
                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- AJAX Scripts for JQuery -->
    <script>
        $(document).ready(function() {
            // Function to handle login form submission via AJAX Post
            $('#login-form').on('submit', function(e) {
                e.preventDefault(); // Prevent standard page refresh
                $('#login-errors').hide().empty();
                
                $.ajax({
                    type: 'POST',
                    url: '{% url "ajax_login" %}',
                    data: $(this).serialize(),
                    success: function(response) {
                        if (response.success) {
                            // If successful, swap views and update username
                            $('#username-display').text(response.username);
                            $('#unauth-view').hide();
                            $('#auth-view').fadeIn();
                            $('#login-form')[0].reset();
                        } else {
                            // If error, display errors natively without refresh
                            let errorsHtml = '<ul class="mb-0 text-start">';
                            for (let field in response.errors) {
                                errorsHtml += '<li>' + response.errors[field].join(' ') + '</li>';
                            }
                            errorsHtml += '</ul>';
                            $('#login-errors').html(errorsHtml).fadeIn();
                        }
                    },
                    error: function() {
                        $('#login-errors').html('An unexpected error occurred.').fadeIn();
                    }
                });
            });

            // Function to handle logout button submission via AJAX Post
            $('#logout-form').on('submit', function(e) {
                e.preventDefault(); // Prevent standard page refresh
                
                $.ajax({
                    type: 'POST',
                    url: '{% url "ajax_logout" %}',
                    data: $(this).serialize(),
                    success: function(response) {
                        if (response.success) {
                            // Swap views back to the connection form mode
                            $('#auth-view').hide();
                            $('#unauth-view').fadeIn();
                        }
                    }
                });
            });
        });
    </script>
</body>
</html>
INNER_EOF
