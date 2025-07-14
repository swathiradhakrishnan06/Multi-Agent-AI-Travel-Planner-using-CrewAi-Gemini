# src/travel_planner/tools/stopover_evaluator.py
from crewai.tools import BaseTool
from typing import List, Dict, Any
import json
import re

class StopoverEvaluator(BaseTool):
    name: str = "stopover_evaluator"
    description: str = "Evaluate flight offers and select top options based on price and interests"

    def _run(self, offers: List[Dict[str, Any]], interests: List[str]) -> List[Dict[str, Any]]:
        """Evaluate flight offers and return top 2 options"""
        try:
            # Handle different input formats
            if isinstance(offers, str):
                # Try to parse JSON string
                try:
                    offers = json.loads(offers)
                except json.JSONDecodeError:
                    # Try to extract offers from text
                    offers = self._extract_offers_from_text(offers)
            
            if not offers:
                return []
            
            scored = []
            for offer in offers:
                try:
                    # Handle different price formats
                    price = self._extract_price(offer)
                    if price is None:
                        continue
                    
                    # Extract stopover information
                    stopover_city = self._extract_stopover_city(offer)
                    
                    # Calculate bonus based on interests
                    bonus = 0
                    if stopover_city and interests:
                        for interest in interests:
                            # Clean interest string (remove emojis and extra text)
                            clean_interest = re.sub(r'[^\w\s]', '', interest.lower())
                            if clean_interest in stopover_city.lower():
                                bonus += 20
                    
                    # Calculate final score (lower is better)
                    score = price - bonus
                    scored.append((score, offer, price, stopover_city))
                    
                except Exception as e:
                    print(f"Error processing offer: {e}")
                    continue
            
            # Sort by score and return top 2
            scored.sort(key=lambda x: x[0])
            top2 = []
            
            for score, offer, price, stopover in scored[:2]:
                result = {
                    "id": offer.get("id", "Unknown"),
                    "price": price,
                    "stopover_city": stopover,
                    "score": score,
                    "summary": f"Flight {offer.get('id', 'Unknown')}: €{price} via {stopover if stopover else 'Direct'}"
                }
                top2.append(result)
            
            return top2
            
        except Exception as e:
            print(f"Error in stopover evaluator: {e}")
            return []
    
    def _extract_price(self, offer: Dict[str, Any]) -> float:
        """Extract price from offer in various formats"""
        try:
            # Try different price field formats
            if "price" in offer:
                price_data = offer["price"]
                if isinstance(price_data, dict):
                    # Try different price keys
                    for key in ["total", "grandTotal", "amount"]:
                        if key in price_data:
                            price_str = str(price_data[key])
                            # Remove currency symbols and convert to float
                            price = re.sub(r'[^\d.]', '', price_str)
                            return float(price)
                elif isinstance(price_data, (int, float)):
                    return float(price_data)
                elif isinstance(price_data, str):
                    price = re.sub(r'[^\d.]', '', price_data)
                    return float(price)
            
            return None
        except:
            return None
    
    def _extract_stopover_city(self, offer: Dict[str, Any]) -> str:
        """Extract stopover city from offer"""
        try:
            if "itineraries" in offer and offer["itineraries"]:
                itinerary = offer["itineraries"][0]
                if "segments" in itinerary:
                    segments = itinerary["segments"]
                    if len(segments) > 1:
                        # Return the destination of the first segment (stopover)
                        first_segment = segments[0]
                        if "arrival" in first_segment:
                            arrival = first_segment["arrival"]
                            if "iataCode" in arrival:
                                return arrival["iataCode"]
            return None
        except:
            return None
    
    def _extract_offers_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract flight offers from text output"""
        offers = []
        lines = text.split('\n')
        
        current_offer = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for flight ID
            if '"id":' in line:
                if current_offer:
                    offers.append(current_offer)
                current_offer = {"id": line.split('"id":')[1].split(',')[0].strip(' "')}
            
            # Look for price
            elif '"total":' in line:
                price_str = line.split('"total":')[1].split(',')[0].strip(' "')
                if "price" not in current_offer:
                    current_offer["price"] = {}
                current_offer["price"]["total"] = price_str
        
        if current_offer:
            offers.append(current_offer)
        
        return offers
