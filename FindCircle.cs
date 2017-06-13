        public class CircleFace
        {
            public OCGeom_Circle cir1 = null;
            public OCGeom_Circle cir2 = null;
            public OCTopoDS_Face faceToFind = null;
        }

        //Example to detect planer start and end face of tube
        // See: https://www.opencascade.com/comment/19852#comment-19852
        {
            List<OCTopoDS_Shape> shapes = OCSerialize.FromStepData(data); //see stepdata below
            Context.Log("shapes.Count: " + shapes.Count);
            OCTopoDS_Shape shape = shapes[0];

            CircleFace[] startEndFace = new CircleFace[2];

            int found=0;
            foreach (OCTopoDS_Face face in shape.Faces())
            {
                // this is an extension method for: OCGeom_Surface s =OCBRep_Tool.Surface(face)
                OCGeom_Surface s = face.Surface();

                // check if face is a plane
                if (s is OCGeom_Plane)
                {
                    OCGeom_Plane plane = s as OCGeom_Plane;
                    List<OCTopoDS_Wire> wires = new List<OCTopoDS_Wire>(face.Wires());

                    // See if the face has 2 wires (outer and inner)
                    if (wires.Count == 2)
                    {
                        OCTopoDS_Edge e1 = wires[0].Edges().First();
                        OCTopoDS_Edge e2 = wires[1].Edges().First();

                        OCGeom_Curve c1 = e1.Curve();
                        OCGeom_Curve c2 = e2.Curve();

                        // see if both wires are Circle's
                        if (c1 is OCGeom_Circle && c2 is OCGeom_Circle)
                        {
                            Context.AddShape(e1, Color.Blue);
                            Context.AddShape(e2, Color.Blue);

                            Context.AddShape(face, Color.Red);

                            OCGeom_Circle cir1 = c1 as OCGeom_Circle;
                            OCGeom_Circle cir2 = c2 as OCGeom_Circle;
                            Context.AddAxis(cir1.Axis(), 25, Color.Green);

                            Context.Log("radius1: " + cir1.Radius());
                            Context.Log("radius2: " + cir2.Radius());

                            startEndFace[found]= new CircleFace();
                            startEndFace[found].cir1=cir1;
                            startEndFace[found].cir1=cir2;
                            startEndFace[found].faceToFind=face;

                            if(found ==1)
                                break;

                            found++;
                        }
                    }
                }
            }

            if (startEndFace[0] != null && startEndFace[1] != null)
            {
                Context.AddLogLine("start and end are found");
                //TODO make algorithm to find the "extrusion path"
            }

            Context.AddShape(shape, Color.Gray, 0.2);
            // Context.AddLogLine(shape.Dump());
        }
