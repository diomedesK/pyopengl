uniform vec3 baseColor;
out vec4 fragColor;

void main(){
  fragColor = vec4(baseColor.rgb, 1.0);
}

