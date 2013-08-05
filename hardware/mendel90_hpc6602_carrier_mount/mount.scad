include <Magpie/magpie.scad>;

ink_spacing_x = 19.5;
ink_spacing_y = 21.5;
ink_hole_dia = 2;
ink_hole_height = 14.8; // from bottom
ink_carrier_width = 30.5;

mount_hole_dia = 4.2;
mount_hole_wall = mount_hole_dia*1.5;
mount_hole_spacing = 50;
mount_extension = 55;
mount_thickness = 6;
mount_height = 50;



difference()
	{
	union()
	{
		hull()
		{
			cylinder(r=mount_hole_wall, h=mount_thickness);
			translate([mount_hole_spacing, 0, 0])
				cylinder(r=mount_hole_wall, h=mount_thickness);
		}
		translate([-mount_hole_wall, 0, 0])
			cube([mount_hole_spacing+mount_hole_wall*2, mount_extension, mount_thickness]);
		translate([-mount_hole_wall, mount_extension, 0])
			cube([mount_hole_spacing+mount_hole_wall*2, mount_thickness, mount_height]);
	}
	translate([0, 0, -eta])
		cylinder(r=mount_hole_dia/2, h=mount_thickness+eta*2);
	translate([mount_hole_spacing, 0, -eta])
		cylinder(r=mount_hole_dia/2, h=mount_thickness+eta*2);
	for(i=[-1, 1])translate([ink_carrier_width/2*i, 0, 0]){
		//we go upside down
		translate([mount_hole_spacing/2+ink_spacing_x/2, mount_extension-eta, mount_height-ink_hole_height])
			rotate([-90, 0, 0])poly_cylinder(r=ink_hole_dia/2, h=mount_thickness+eta*2);

		translate([mount_hole_spacing/2-ink_spacing_x/2, mount_extension-eta, mount_height-ink_hole_height])
			rotate([-90, 0, 0])poly_cylinder(r=ink_hole_dia/2, h=mount_thickness+eta*2);

		translate([mount_hole_spacing/2+ink_spacing_x/2, mount_extension-eta, mount_height-ink_hole_height-ink_spacing_y])
		rotate([-90, 0, 0])poly_cylinder(r=ink_hole_dia/2, h=mount_thickness+eta*2);

		translate([mount_hole_spacing/2-ink_spacing_x/2, mount_extension-eta, mount_height-ink_hole_height-ink_spacing_y])
			rotate([-90, 0, 0])poly_cylinder(r=ink_hole_dia/2, h=mount_thickness+eta*2);	
	}
}
