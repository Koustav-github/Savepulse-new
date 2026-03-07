import jwt from "jsonwebtoken";
import { Request, Response } from "express";
import { db } from "../../db/db"; 
import { hospitals } from "../../schema/schema"; // Correct table import
import { eq } from "drizzle-orm";

export default async function hospitalSignIn(req: Request, res: Response) {
  try {
    const { hospital_name } = req.body; 
    
    if (!hospital_name) {
      return res.status(400).json({ message: "Hospital name is required to sign in" });
    }

    const existingHospital = await db
      .select()
      .from(hospitals)
      .where(eq(hospitals.hospital_name, hospital_name))
      .limit(1);

    if (!existingHospital.length) {
      return res.status(401).json({ message: "Hospital not found. Please register first."});
    }

    const hospitalData = existingHospital[0];

    const token = jwt.sign(
      { 
        hospitalId: hospitalData.hospital_id, 
        name: hospitalData.hospital_name 
      },
      process.env.JWT_SECRET!,
      { expiresIn: "7d" }
    );

    res.cookie("hospital_token", token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
      path: "/",
    });

    return res.status(200).json({ 
      message: "Hospital signed in successfully",
      hospital: { 
        id: hospitalData.hospital_id, 
        name: hospitalData.hospital_name 
      } 
    });

  } catch (err: any) {
    console.error("Hospital Sign-in error:", err);
    return res.status(500).json({ message: "Internal server error" });
  }
}