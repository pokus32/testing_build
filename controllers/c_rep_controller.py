import json
from kivy.uix.boxlayout import BoxLayout
from loguru import logger


class CRController():
	''' posrednik mejdu view i servisami '''
	
	def __init__(self, model, dimHeader, colHeader):
		logger.info('')
		self.model 	= model
		self.dimHeader = dimHeader
		self.colHeader = colHeader
		self.view 	= None

	async def fill_view(self, part_name, tool_id, operator):
		logger.info('')
		self.view.part_name = part_name
		self.view.mtool_id = tool_id
		self.view.operator = operator
		self.view.rows_layout.clear_widgets()
		res = await self.model.get_cr_data(tool_id)
		if not res:
			return
		dims, values = res

		if not all([dims, values]):
			return

		dims = list(map(json.loads, dims.split('|')))
		values = list(map(json.loads, values.split('|')))
		i = 1
		rows = []
		for dim in dims:
			dim_id = dim.get('dim_id', '---')
			if i % 2:
				bg_color = [0.70,0.89,0.82,1]
			else:
				bg_color = [0.81,0.89,0.82,1]
			tmp_obj = self.dimHeader()
			tmp_obj.col_main_header.remove_widget(tmp_obj.main_header)
			tmp_obj.col_layout.clear_widgets()
			tmp_obj.col_main_header.rows = 1
			tmp_obj.norm_background_color = bg_color
			prefix = str(dim.get('prefix', ''))
			value = str(dim.get('value', '---'))
			postfix = str(dim.get('postfix', '---'))
			tmp_obj.dim_n.text = str(dim_id)
			tmp_obj.nom.text = f'{prefix}{value}{postfix}'
			tmp_obj.tol.text = str(dim.get('up', '---')) + '\n' + str(dim.get('low', '---'))

			for value in values:
				value = value.get(dim_id, {})
				tmp_lbl = self.colHeader()
				if value.get('state', 'nok') == 'ok':
					tmp_lbl.n_b_color = bg_color
				else:
					tmp_lbl.n_b_color = [0.91,0.79,0.72,1]
				tmp_lbl.text = str(value.get('value', '---'))
				tmp_obj.col_layout.add_widget(tmp_lbl)

			rows.append(tmp_obj)
			self.view.rows_layout.add_widget(tmp_obj)
			i += 1
			if i < 5: self.view.rows_layout.add_widget(BoxLayout())

