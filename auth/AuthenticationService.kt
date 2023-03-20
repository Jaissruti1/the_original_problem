package com.uncc.jobboard.auth


import com.uncc.jobboard.config.JwtService
import com.uncc.jobboard.token.Token
import com.uncc.jobboard.token.TokenRepository
import com.uncc.jobboard.token.TokenType
import com.uncc.jobboard.user.Role
import com.uncc.jobboard.user.User
import com.uncc.jobboard.user.UserRepository
import org.springframework.security.authentication.AuthenticationManager
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Service

@Service
class AuthenticationService (
        private val repository: UserRepository,
        private val tokenRepository: TokenRepository,
        private val passwordEncoder: PasswordEncoder,
        private val jwtService: JwtService,
        private val authenticationManager: AuthenticationManager
) {

    fun register(request: RegisterRequest): AuthenticationResponse {

        val user = User(
                firstname = request.firstname,
                lastname = request.lastname,
                email = request.email,
                password = passwordEncoder.encode(request.password),
                role = Role.USER
        )
        val savedUser: User = repository.save(user)
        val jwtToken: String = jwtService.generateToken(user)
        saveUserToken(savedUser, jwtToken)
        return AuthenticationResponse(jwtToken)
    }

    fun authenticate(request: AuthenticationRequest): AuthenticationResponse {
        authenticationManager.authenticate(
                UsernamePasswordAuthenticationToken(
                        request.email,
                        request.password
                )
        )

        val user = repository.findByEmail(request.email)?.orElseThrow()

        if (user != null) {
            val jwtToken: String = jwtService.generateToken(user)
            revokeAllUserTokens(user)
            saveUserToken(user, jwtToken)
            return AuthenticationResponse(token = jwtToken)
        }

        return AuthenticationResponse(token = "")

    }

    private fun saveUserToken(user: User, jwtToken: String) {

        val token = Token(
                user = user,
                token = jwtToken,
                tokenType = TokenType.BEARER,
                expired = false,
                revoked = false
        )
        tokenRepository.save(token)
    }

    private fun revokeAllUserTokens(user: User) {
        val validUserTokens : Iterable<Token?>? = tokenRepository.findAllValidTokenByUser(user.id)
        if (validUserTokens != null) {
            validUserTokens?.forEach { token ->
                token?.expired = true
                token?.revoked = true
            }
            tokenRepository.saveAll(validUserTokens)
        }

    }
}