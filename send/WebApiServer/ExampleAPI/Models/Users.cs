using System;
using System.Collections.Generic;

// Code scaffolded by EF Core assumes nullable reference types (NRTs) are not used or disabled.
// If you have enabled NRTs for your project, then un-comment the following line:
// #nullable disable

namespace ExampleAPI.Models
{
    public partial class Users
    {
        public Users()
        {
            RefreshToken = new HashSet<RefreshToken>();
        }

        public int Id { get; set; }
        public string Login { get; set; }
        public string Password { get; set; }
        public string Email { get; set; }

        public virtual ICollection<RefreshToken> RefreshToken { get; set; }
    }
}
