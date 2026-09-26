// Relmote Pocket envelope v0.1
// Concept-only parametric massing model; NOT a manufacturable enclosure.

$fn = 48;

body_h = 150;
body_w = 72;
body_t = 18;
corner_r = 8;

module_t = 6;
module_gap = 4;
s_zone = 68;
rear_margin = 2;

display_w = 52;
display_h = 28;
display_depth = 0.8;

button_auth_w = 20;
button_auth_h = 9;
button_stop_d = 13;

module rounded_box(w, h, t, r) {
    linear_extrude(height=t)
        offset(r=r)
            square([w-2*r, h-2*r], center=true);
}

module body() {
    translate([0,0,body_t/2])
        rounded_box(body_w, body_h, body_t, corner_r);
}

module display_window() {
    translate([0, 28, body_t + display_depth/2])
        cube([display_w, display_h, display_depth], center=true);
}

module authorize_button() {
    translate([-18, -52, body_t + 1])
        cube([button_auth_w, button_auth_h, 2], center=true);
}

module stop_button() {
    translate([22, -52, body_t + 1])
        cylinder(h=2, d=button_stop_d, center=true);
}

module snap_module(top=true) {
    y = top ? (module_gap/2 + s_zone/2) : -(module_gap/2 + s_zone/2);
    translate([0, y, -module_t/2])
        rounded_box(s_zone, s_zone, module_t, 5);
}

// Core body
color("gray") body();

// Front UI massing
color("black") display_window();
color("green") authorize_button();
color("red") stop_button();

// Uncomment to visualize snap modules on rear.
// color("darkslategray", 0.8) snap_module(true);
// color("slategray", 0.8) snap_module(false);
