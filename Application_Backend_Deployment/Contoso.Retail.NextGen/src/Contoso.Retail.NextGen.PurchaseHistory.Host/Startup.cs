using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Cosmonaut;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Controllers;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.OpenApi.Models;

namespace Contoso.Retail.NextGen.PurchaseHistory.Host
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }
        private readonly string myPolicy = "AllowAnyOrigins";

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(options =>
            {
                options.AddPolicy(name: myPolicy,
                    builder =>
                    {
                        builder.AllowAnyOrigin();
                        builder.AllowAnyHeader();
                        builder.AllowAnyMethod();
                    });
            });

            services.AddControllers();

            //Register swagger gen
            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new OpenApiInfo { Title = "Contoso Retail's PurchaseHistory Service API Endpoint", Version = "v1" });
                c.CustomOperationIds(d => (d.ActionDescriptor as ControllerActionDescriptor)?.ActionName);
            });

            services.AddSwaggerGenNewtonsoftSupport();

            services.AddSingleton<ICosmosStore<Models.PurchaseHistory>, CosmosStore<Models.PurchaseHistory>>(c => {

                var serviceuri = Configuration["Values:CosmosCoreAPIUri"];
                var accesskey = Configuration["Values:CosmosCoreAccessKey"];
                var dbName = Configuration["Values:CosmosDatabaseName"];

                var cosmosSettings = new CosmosStoreSettings(dbName,
                       serviceuri,
                       accesskey);

                return new CosmosStore<Models.PurchaseHistory>(cosmosSettings);
            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            app.UseCors(myPolicy);

            app.UseMiddleware(typeof(Contoso.HttpHost.Middleware.Exception.ExceptionHandler));

            //app.UseHttpsRedirection();

            app.UseRouting();


            app.UseAuthorization();

            app.UseSwagger();

            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint("./v1/swagger.json", "Contoso Retail's Purchase History Service API V1");

            });

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
