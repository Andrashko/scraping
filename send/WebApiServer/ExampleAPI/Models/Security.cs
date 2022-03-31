using System;
using System.Security.Cryptography;
using System.Text;

namespace ExampleAPI.Models
{
    public class Security
    {
        protected string _salt;

        public Security(string salt)
        {
            _salt = salt;
        }
        public string EncodePassword(string password)
        {
            var key = Encoding.UTF8.GetBytes(_salt);
            var pass= Encoding.UTF8.GetBytes(password);
            var hmacSHA1 = new HMACSHA1(key);
            var saltedHash = hmacSHA1.ComputeHash(pass);
            return Convert.ToBase64String(saltedHash);            
        }

        public bool CheckPassword(string password, string encodedPassword)
        {
            return encodedPassword == this.EncodePassword(password);
        }

    }
}
