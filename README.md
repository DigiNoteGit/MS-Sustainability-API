# Microsoft Azure Carbon Footprint Measurement via Microsoft Cloud for Sustainability API
Basic Python script to access Microsoft Cloud for Sustainability (MCFS) API with a service principal

Requirements:  
1 - Request access to MCFS via:  https://forms.office.com/r/rTVhjxVjGw  
2 - Register MCFS SDS app in your tenant (follow instructions of MCFS onboarding):  
3 - Create a service principal and generate an app secret  
4 - Grant App.Emission.Read permission (for MCFS SDS) to your service principal (In EntraID/AppRegistrations/YourApp/APIpermissions)  

For more details please look into the comments we left in the python script
