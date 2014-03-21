var model = [
{
	"category": "Abonnementer/Internett",
			 "amount": -2610.00 	,
			 "payments_per_year": 2 	,
			 "per_month": -435.00
},
{
	"category": "Abonnementer/Spotify",
	"amount": -99.00 	,
	"payments_per_year": 12 	,
	"per_month": -99.00
},
{
	"category": "Barnehage",
	"amount": -3451.00 	,
	"payments_per_year": 12 	,
	"per_month": -3451.00
},
{
	"category": "Barnetrygd",
	"amount": 1940.00 	,
	"payments_per_year": 12 	,
	"per_month": 1940.00
},
{
	"category": "Forsikringer/Barn",
	"amount": -5976.00 	,
	"payments_per_year": 1 	,
	"per_month": -498.00
},
{
	"category": "Forsikringer/Bil",
	"amount": -4596.00 	,
	"payments_per_year": 1 	,
	"per_month": -383.00
},
{
	"category": "Forsikringer/Livs",
	"amount": -533.43 	,
	"payments_per_year": 12 	,
	"per_month": -533.43
},
{
	"category": "Husholdning/Mat",
	"amount": -10000.00 	,
	"payments_per_year": 12 	,
	"per_month": -10000.00
},
{
	"category": "Lån/Startlån",
	"amount": -1452.00 	,
	"payments_per_year": 12 	,
	"per_month": -1452.00
},
{
	"category": "Lån/Studielån",
	"amount": -3021.00 	,
	"payments_per_year": 4 	,
	"per_month": -1007.00
},
{
	"category": "Lønn/Bouvet",
	"amount": 24510.33 	,
	"payments_per_year": 12 	,
	"per_month": 24510.33
},
{
	"category": "Lønn/Nav",
	"amount": 5758.00 	,
	"payments_per_year": 24 	,
	"per_month": 11516.00
},
{
	"category": "Mobiltelefon",
	"amount": -400.00 	,
	"payments_per_year": 12 	,
	"per_month": -400.00
},
{
	"category": "Strøm",
	"amount": -1000.00 	,
	"payments_per_year": 12 	,
	"per_month": -1000.00
},
{
	"category": "Transport/Bil",
	"amount": -2500.00 	,
	"payments_per_year": 12 	,
	"per_month": -2500.00
},
{
	"category": "Velforening",
	"amount": -500.00 	,
	"payments_per_year": 12 	,
	"per_month": -500.00
} ];

// var budgetTable = new sap.m.Table();
var budgetTable = new sap.m.Table({
	    headerText: "Budget detail",
});

budgetTable.setModel(new sap.ui.model.json.JSONModel(model));
budgetTable.placeAt("table");

