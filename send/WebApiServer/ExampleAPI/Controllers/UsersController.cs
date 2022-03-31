using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ExampleAPI.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Options;
using System.IdentityModel.Tokens.Jwt;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using System.Security.Claims;
using System.Security.Cryptography;

namespace ExampleAPI.Controllers
{
    
    [Route("api/[controller]")]
    [ApiController]
    public class UsersController : ControllerBase
    {
        private readonly EPROJECTSSCRAPING2022SENDWEBAPISERVEREXAMPLEAPIEXAMPLEMDFContext _context;

        private readonly JWTSettings _jwtSettings;

        private readonly Security _security;
        public UsersController(EPROJECTSSCRAPING2022SENDWEBAPISERVEREXAMPLEAPIEXAMPLEMDFContext context, IOptions<JWTSettings> jwtsettings)
        {
            _context = context;
            _jwtSettings = jwtsettings.Value;
            _security = new Security (_jwtSettings.SecretKey);
        }

        [Authorize]
        [HttpGet]
        public async Task<ActionResult<Users>> GetUsers()
        {
            string login = HttpContext.User.Identity.Name;
            var user = await _context.Users.Where(user => user.Login==login).FirstOrDefaultAsync();
            if (user==null)
                return NotFound();
            return Ok(user);
        }


        // POST: api/Users/Login
        [HttpPost ("Login")]
        public async Task<ActionResult<UserWithTocken>> Login( [FromBody] Users user)
        {
            var userdb = await _context.Users.Where(u => u.Login == user.Login).FirstOrDefaultAsync();
            if (userdb==null || ! _security.CheckPassword (user.Password, userdb.Password))
                return BadRequest("Wrong password or login");

            //refresh token
            RefreshToken refreshToken = GenerateRefreshToken();
            userdb.RefreshToken.Add(refreshToken);
            await _context.SaveChangesAsync();

            UserWithTocken result = new UserWithTocken(userdb);
            result.Token = GenerateJWTToken(userdb.Id);
            result.RefreshToken = refreshToken.Token;  

            return Ok(result);
        }

        // POST: api/Users/Register
        [HttpPost("Register")]
        public async Task<ActionResult<Users>> Register([FromBody] Users user)
        {
            user.Password = _security.EncodePassword(user.Password);

            _context.Users.Add(user);

            await _context.SaveChangesAsync();

            return Ok(user);
        }

        // POST: api/Users/Refresh
        [HttpPost("Refresh")]
        public async Task<ActionResult<UserWithTocken>> Refresh([FromBody] RefreshRequest request)
        {
            Users user = await GetUserFromToken(request.Token);
            if (user == null || ! await ValidateRefreshToken(user.Id, request.RefreshToken))
                return null;
            UserWithTocken result = new UserWithTocken(user);
            result.Token = GenerateJWTToken(user.Id);
            return result;
        }

        private RefreshToken GenerateRefreshToken()
        {
            var refreshToken = new RefreshToken();
            var rng = RandomNumberGenerator.Create();
            var randomNumber = new byte[32];
            rng.GetBytes(randomNumber);
            refreshToken.Token = Convert.ToBase64String(randomNumber);
            refreshToken.ExpiryDate = DateTime.Now.AddDays(30);
            return refreshToken;
        }

        private string GenerateJWTToken(int Id)
        {
            var tokenHandler = new JwtSecurityTokenHandler();
            var key = Encoding.UTF8.GetBytes(_jwtSettings.SecretKey);
            var tokenDescriptor = new SecurityTokenDescriptor
            {
                Subject = new ClaimsIdentity(new Claim[]
                {
                    new Claim(ClaimTypes.Name, Convert.ToString(Id))
                }),
                Expires = DateTime.Now.AddMinutes(10),
                SigningCredentials = new SigningCredentials(new SymmetricSecurityKey(key), SecurityAlgorithms.HmacSha256Signature)
            };
            var token = tokenHandler.CreateToken(tokenDescriptor);
            return tokenHandler.WriteToken(token);
        }

        private async Task<Users> GetUserFromToken(string token)
        {
            var tokenHandler = new JwtSecurityTokenHandler();
            var key = Encoding.UTF8.GetBytes(_jwtSettings.SecretKey);
            var tokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(key),
                ValidateIssuer = false,
                ValidateAudience = false,
                ValidateLifetime = false, //
                ClockSkew = TimeSpan.Zero
            };
            SecurityToken securityToken;
            var principle = tokenHandler.ValidateToken(token, tokenValidationParameters,  out securityToken);
            JwtSecurityToken jwtSecurityToken = securityToken as JwtSecurityToken;
            if (jwtSecurityToken == null )
                return null;
            int userId = Convert.ToInt32( principle.FindFirst(ClaimTypes.Name)?.Value );
            return await _context.Users.Where(user => user.Id == userId).FirstOrDefaultAsync();
        }

        private async Task<bool> ValidateRefreshToken(int id, string token)
        {
            RefreshToken refreshToken = await _context.RefreshToken
                .Where(rt => rt.Token == token)
                .OrderByDescending(rt => rt.ExpiryDate)
                .FirstOrDefaultAsync();

            return refreshToken != null &&
                refreshToken.User.Id == id &&
                refreshToken.ExpiryDate > DateTime.Now;
        }
    }
}
