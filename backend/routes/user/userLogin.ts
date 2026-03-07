import jwt from "jsonwebtoken";
import { Request, Response } from "express";
import { db } from "../../db/db"; 
import { user } from "../../schema/schema";
import { eq } from "drizzle-orm";

export default async function userSignIn(req: Request, res: Response) {
  try {
    const { email } = req.body;
    if (!email) return res.status(400).json({ message: "Email is required" });

    const existingUser = await db.select().from(user).where(eq(user.email, email)).limit(1);

    if (!existingUser.length) {
      return res.status(401).json({ message: "User not found." });
    }

    const userData = existingUser[0];

    // Generate JWT
    const token = jwt.sign(
      { userId: userData.id, email: userData.email},
      process.env.JWT_SECRET!,
      { expiresIn: "7d" }
    );

    // 🍪 Set HTTP-Only Cookie
    res.cookie("token", token, {
      httpOnly: true,      // Prevents JavaScript from reading the cookie
      secure: process.env.NODE_ENV === "production", // Only send over HTTPS in prod
      sameSite: "lax",     // Protects against CSRF
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
      path: "/",           // Accessible across the whole site
    });

    return res.status(200).json({ 
      message: "Signed in successfully",
      user: { id: userData.id, email: userData.email } 
    });

  } catch (err: any) {
    console.error("Sign-in error:", err);
    return res.status(500).json({ message: "Internal server error" });
  }
}