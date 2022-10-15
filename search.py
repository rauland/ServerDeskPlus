from dataclasses import dataclass
import epoch

# Default object parms for SD query
@dataclass
class Parms : # class Search:
	start_index: int = 1
	row_count: int = 100
	day: int = 1
	month: int = 0
	choice: str = "open"
	fields_required: str ='[get_all]'

def query(d) : 
	data = {
		"list_info":{
			"row_count": d.row_count,
			"start_index": d.start_index,
			"sort_field": "id",
			"sort_order": "desc",
			"get_total_count": True,
			"fields_required":d.fields_required,
      	}
    } 
	match d.choice:
		case 'open':
			data["list_info"]['filter_by'] ={
					"name": "Open_System"
				}
		case 'created':
			data["list_info"]['search_criteria'] =[{
				"field": "created_time",
				"condition": "greater than",
				"value": epoch.getlastdate(1, d.month),                        
				},
				{
				"field": "created_time",
				"condition": "lesser than",
				"value": epoch.getlastdate(1, d.month - 1),
				"logical_operator" : "and"                        
				}
			]
		case 'closed':
			data["list_info"]['search_criteria'] =[{
				"field": "resolved_time",
				"condition": "greater than",
				"value": epoch.getlastdate(1, d.month),                        
				},
				{
				"field": "resolved_time",
				"condition": "lesser than",
				"value": epoch.getlastdate(1, d.month - 1),
				"logical_operator" : "and"                        
				}
			]
		case 'all':
			data["list_info"]['search_criteria'] =[{      
				"field": "created_time",
				"condition": "greater than",
				"value": epoch.getlastdate(1, d.month),                        
				},
			]   
	
	return data