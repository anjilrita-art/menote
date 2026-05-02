import { useState } from "react";
import { motion } from "framer-motion";
import { ShoppingCart, Camera, Film, Mail } from "lucide-react";

export default function Home() {
  const [cart, setCart] = useState([]);

  const addToCart = (item) => {
    setCart([...cart, item]);
  };

  return (
    <div className="min-h-screen bg-neutral-50 text-neutral-900 font-sans">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-4 shadow-md bg-white sticky top-0 z-50">
        <h1 className="text-2xl font-bold tracking-tight">asfu.flimaking</h1>
        <div className="flex items-center gap-6">
          <a href="#portfolio" className="hover:text-neutral-500">Portfolio</a>
          <a href="#shop" className="hover:text-neutral-500">Shop</a>
          <a href="#about" className="hover:text-neutral-500">About</a>
          <a href="#contact" className="hover:text-neutral-500">Contact</a>
          <button className="relative">
            <ShoppingCart className="w-6 h-6" />
            {cart.length > 0 && (
              <span className="absolute -top-2 -right-2 text-xs bg-black text-white rounded-full px-2">
                {cart.length}
              </span>
            )}
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="h-[90vh] flex flex-col items-center justify-center text-center bg-gradient-to-r from-neutral-900 to-neutral-700 text-white">
        <motion.h2 initial={{opacity:0, y:20}} animate={{opacity:1,y:0}} transition={{duration:1}} className="text-5xl font-extrabold">
          Capture Moments, Tell Stories
        </motion.h2>
        <p className="mt-4 text-lg max-w-xl">
          Photography & Filmmaking by Asfu — modern visuals that speak louder than words.
        </p>
        <a href="#portfolio" className="mt-6 px-6 py-3 bg-white text-black rounded-2xl shadow hover:bg-neutral-200">
          Explore Work
        </a>
      </section>

      {/* Portfolio */}
      <section id="portfolio" className="px-8 py-16">
        <h3 className="text-3xl font-bold mb-8">Portfolio</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="rounded-2xl overflow-hidden shadow-lg group">
            <img src="/photo1.jpg" alt="Photography" className="group-hover:scale-105 transition-transform" />
            <div className="p-4 flex items-center gap-2 font-semibold"><Camera className="w-5"/> Photography</div>
          </div>
          <div className="rounded-2xl overflow-hidden shadow-lg group">
            <img src="/video1.jpg" alt="Videography" className="group-hover:scale-105 transition-transform" />
            <div className="p-4 flex items-center gap-2 font-semibold"><Film className="w-5"/> Videography</div>
          </div>
          <div className="rounded-2xl overflow-hidden shadow-lg group">
            <img src="/photo2.jpg" alt="Creative" className="group-hover:scale-105 transition-transform" />
            <div className="p-4 font-semibold">Creative Shots</div>
          </div>
        </div>
      </section>

      {/* Shop */}
      <section id="shop" className="px-8 py-16 bg-neutral-100">
        <h3 className="text-3xl font-bold mb-8">Shop</h3>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            {id:1, name:"Sunset Print", price:"$20", img:"/shop1.jpg"},
            {id:2, name:"Cityscape", price:"$25", img:"/shop2.jpg"},
            {id:3, name:"Short Film", price:"$50", img:"/shop3.jpg"},
          ].map(item => (
            <div key={item.id} className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <img src={item.img} alt={item.name} className="w-full h-48 object-cover" />
              <div className="p-4">
                <h4 className="font-semibold">{item.name}</h4>
                <p className="text-neutral-600">{item.price}</p>
                <button onClick={() => addToCart(item)} className="mt-3 px-4 py-2 bg-black text-white rounded-xl hover:bg-neutral-800">
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* About */}
      <section id="about" className="px-8 py-16">
        <h3 className="text-3xl font-bold mb-6">About</h3>
        <p className="max-w-2xl text-lg leading-relaxed">
          Hi, I’m Asfu — a passionate photographer & filmmaker. My mission is to create visuals that don’t just look beautiful, but also evoke emotions and tell untold stories. From portraits to cinematic storytelling, every frame is crafted with love.
        </p>
      </section>

      {/* Contact */}
      <section id="contact" className="px-8 py-16 bg-neutral-900 text-white">
        <h3 className="text-3xl font-bold mb-6">Get in Touch</h3>
        <form className="max-w-xl grid gap-4">
          <input type="text" placeholder="Your Name" className="px-4 py-3 rounded-xl text-black" />
          <input type="email" placeholder="Your Email" className="px-4 py-3 rounded-xl text-black" />
          <textarea placeholder="Your Message" rows="4" className="px-4 py-3 rounded-xl text-black"></textarea>
          <button className="px-6 py-3 bg-white text-black rounded-xl shadow hover:bg-neutral-200 flex items-center gap-2">
            <Mail className="w-5"/> Send Message
          </button>
        </form>
      </section>

      <footer className="py-6 text-center text-neutral-500 text-sm">
        © {new Date().getFullYear()} asfu.flimaking — All Rights Reserved.
      </footer>
    </div>
  );
}
