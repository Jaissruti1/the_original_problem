package com.uncc.jobboard.auth

data class AuthenticationRequest (
    var email: String,
    var password: String
)