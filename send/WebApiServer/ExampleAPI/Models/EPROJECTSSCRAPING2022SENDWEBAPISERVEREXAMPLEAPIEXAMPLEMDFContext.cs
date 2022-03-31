using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

// Code scaffolded by EF Core assumes nullable reference types (NRTs) are not used or disabled.
// If you have enabled NRTs for your project, then un-comment the following line:
// #nullable disable

namespace ExampleAPI.Models
{
    public partial class EPROJECTSSCRAPING2022SENDWEBAPISERVEREXAMPLEAPIEXAMPLEMDFContext : DbContext
    {
        public EPROJECTSSCRAPING2022SENDWEBAPISERVEREXAMPLEAPIEXAMPLEMDFContext()
        {
        }

        public EPROJECTSSCRAPING2022SENDWEBAPISERVEREXAMPLEAPIEXAMPLEMDFContext(DbContextOptions<EPROJECTSSCRAPING2022SENDWEBAPISERVEREXAMPLEAPIEXAMPLEMDFContext> options)
            : base(options)
        {
        }

        public virtual DbSet<RefreshToken> RefreshToken { get; set; }
        public virtual DbSet<Shop> Shop { get; set; }
        public virtual DbSet<Users> Users { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer("Name=ExampleDB");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<RefreshToken>(entity =>
            {
                entity.Property(e => e.ExpiryDate)
                    .HasColumnName("Expiry_date")
                    .HasColumnType("date");

                entity.Property(e => e.Token).IsRequired();

                entity.Property(e => e.UserId).HasColumnName("User_id");

                entity.HasOne(d => d.User)
                    .WithMany(p => p.RefreshToken)
                    .HasForeignKey(d => d.UserId)
                    .HasConstraintName("FK_RefreshToken_User");
            });

            modelBuilder.Entity<Shop>(entity =>
            {
                entity.Property(e => e.Name)
                    .HasColumnName("name")
                    .HasMaxLength(50);

                entity.Property(e => e.Price)
                    .HasColumnName("price")
                    .HasMaxLength(50);
            });

            modelBuilder.Entity<Users>(entity =>
            {
                entity.Property(e => e.Email).HasMaxLength(50);

                entity.Property(e => e.Login).HasMaxLength(50);

                entity.Property(e => e.Password).HasMaxLength(50);
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
