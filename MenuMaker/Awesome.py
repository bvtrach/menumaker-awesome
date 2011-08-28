import MenuMaker




from MenuMaker import indent, writeFullMenu




menuFile = "~/.config/awesome/menumaker/menu.lua"




def _map(x) :
	for d, s in (("&amp;", "&"), ("\'", "\"")) :
		x = x.replace(s, d)
	return x




class Sep(object) :
	def emit(self, level) :
		return ['%s' % indent(level)]
	def emit_menu(self, level) :
		return ['']



class App(object) :
	def emit(self, level) :
		x = indent(1)
		cmd = self.app.execmd
		if self.app.terminal :
			cmd = MenuMaker.terminal.runCmd(cmd)
		return ['%s{ "%s", "%s"},' % (x, _map(self.app.name),cmd)]
	def emit_menu(self,level) :
		return []




class Menu(object) :
	id = 0
	def __init__(self) :
		super(Menu, self).__init__()
		self.id = Menu.id
		Menu.id += 1
	def emit_menu(self, level) :
		menu = ['']
		if len(self) != 0:
			for x in self :
				menu += x.emit_menu(level)
			menu.append('')
			menu += ['%smmenu["%s"] = {' % (indent(level), _map(self.name))]
			for x in self :
				menu += x.emit(level)
			menu.append('%s}' % indent(level))
			return menu
		else: 
			return []
	def emit(self, level) :
		menu = ['%s{ "%s", mmenu["%s"]},' % (indent(level), _map(self.name),_map(self.name))]
		return menu




class Root(object) :
	name = "awesome_apps"
	def __init__(self, subs) :
		super(Root, self).__init__(subs)
		self.id = "rootmenu"
	def emit(self, level) :
		menu=['module("menumaker.menu")',
		      'mmenu = {}']
		if writeFullMenu :
			for x in self :
				menu += x.emit_menu(level)
			menu.append('mmenu["main"] = {')
			for x in self :
				menu += x.emit(level+1)			
			menu.append('}')
			return menu
		else :
			for x in self :
				menu += x.emit_menu(level)
			menu.append('')
			menu = ['%s mmenu%s = {' % (indent(level), self.id)]
			for x in self :
				menu += x.emit(level + 1)
				menu.append('%s}' % indent(level))
			return menu





class SysMenu(MenuMaker.Menu) :
	name = "Awesome"
	def __init__(self) :
		subs = [
			X('   { "manual", terminal .. " -e man awesome" },'),
			X('   { "edit config", editor_cmd .. " " .. awful.util.getdir("config") .. "/rc.lua" },'),
			X('   { "restart", awesome.restart },'),
			X('   { "quit", awesome.quit }')
		]
		super(SysMenu, self).__init__(subs)
		self.align = MenuMaker.Entry.StickBottom




class X(MenuMaker.Entry) :
	def __init__(self, x) :
		super(X, self).__init__()
		self.align = MenuMaker.Entry.StickBottom
		self.x = x
	def emit_menu(self, level) :
		return ['']
	def emit(self, level) :
		return [indent(level) + self.x]
