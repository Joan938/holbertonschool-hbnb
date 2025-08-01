HBnB - Simple Web Client

Part 4 - Simple Web Client

In this phase, I focus on the front-end development of my application using HTML5, CSS3, and JavaScript ES6. My goal is to design and implement an interactive user interface that connects with the back-end services I developed in earlier parts of the project.

Objectives

Develop a user-friendly interface following the design specifications I received.

Implement client-side functionality to interact with my back-end API.

Ensure secure and efficient data handling using JavaScript.

Apply modern web development practices to create a dynamic web application.

Learning Goals

Apply HTML5, CSS3, and JavaScript ES6 in a real-world context.

Use AJAX/Fetch API to communicate with back-end services.

Implement authentication and manage user sessions securely.

Enhance user experience with client-side scripting to avoid full page reloads.

Tasks Breakdown

1. Design

Complete the provided HTML and CSS files to match the design specifications.

Create pages for:

Login

List of Places

Place Details

Add Review

2. Login

Implement login functionality by consuming the back-end API.

Store the JWT token returned by the API in a cookie for session management.

3. List of Places

Build the main page to display all available places.

Fetch places data from the API and add client-side filtering by country.

Redirect users to the login page if they are not authenticated.

4. Place Details

Create a detailed view for each place.

Fetch specific place details using the place ID from the API.

Provide access to the Add Review form only when the user is authenticated.

5. Add Review

Implement a form to submit a review for a selected place.

Ensure the form is accessible only to authenticated users, otherwise redirect to the home page.

CORS Configuration

While testing the client against my API, I might encounter Cross-Origin Resource Sharing (CORS) errors. To fix this, I will update my Flask API to allow requests from my front end. For guidance, I refer to the MDN CORS article.

Resources

HTML5 Documentation

CSS3 Documentation

JavaScript ES6 Features

Fetch API

Responsive Web Design Basics

Handling Cookies in JavaScript

Client-Side Form Validation

