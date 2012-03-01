function drawMenu(i) {
	document.write("<P><CENTER>");
	if (i != 1) {
		document.write("<A HREF='.'>");
	}
	document.write("Home/Book");
	if (i != 1) {
		document.write("</A>");
	}
	document.write("&nbsp;&nbsp;&nbsp;");
	if (i != 2) {
		document.write("<A HREF='plan.html'>");
	}
	document.write("Study Plan");
	if (i != 2) {
		document.write("</A>");
	}
	document.write("&nbsp;&nbsp;&nbsp;");
	if (i != 3) {
		document.write("<A HREF='software.html'>");
	}
	document.write("Software");
	if (i != 3) {
		document.write("</A>");
	}
	document.write("&nbsp;&nbsp;&nbsp;");
	if (i != 4) {
		document.write("<A HREF='about.html'>");
	}
	document.write("About");
	if (i != 4) {
		document.write("</A>");
	}
	document.write("&nbsp;&nbsp;&nbsp;");
	if (i != 5) {
		document.write("<A HREF='help.html'>");
	}
	document.write("Help/Contact");
	if (i != 5) {
		document.write("</A>");
	}
	document.write("</CENTER></P>");
}
