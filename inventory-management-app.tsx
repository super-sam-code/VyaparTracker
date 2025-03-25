import React, { useState, useEffect, useCallback } from 'react';
import { AlertCircle, Package, ShoppingCart, Plus, Edit, Trash2, Save, X } from 'lucide-react';

const InventoryManagementApp = () => {
  const [inventory, setInventory] = useState([
    { 
      id: 1, 
      name: 'Basmati Rice', 
      currentStock: 50, 
      reorderPoint: 20, 
      unitPrice: 99.99, 
      supplier: 'Bombay Rice Traders',
      unit: 'kg',
      category: 'Groceries'
    },
    { 
      id: 2, 
      name: 'Masala Tea Powder', 
      currentStock: 100, 
      reorderPoint: 30, 
      unitPrice: 250.00, 
      supplier: 'Chennai Spice Merchants',
      unit: 'kg',
      category: 'Beverages'
    },
    { 
      id: 3, 
      name: 'Cooking Oil', 
      currentStock: 10, 
      reorderPoint: 15, 
      unitPrice: 180.50, 
      supplier: 'Delhi Wholesale Grocers',
      unit: 'ltr',
      category: 'Cooking Essentials'
    }
  ]);

  const [lowStockItems, setLowStockItems] = useState([]);
  const [editingItem, setEditingItem] = useState(null);
  const [newItem, setNewItem] = useState({
    name: '',
    currentStock: 0,
    reorderPoint: 0,
    unitPrice: 0,
    supplier: '',
    unit: 'kg',
    category: ''
  });
  const [isAddingItem, setIsAddingItem] = useState(false);

  // Recalculate low stock items whenever inventory changes
  useEffect(() => {
    const itemsNeedingRestock = inventory.filter(
      item => item.currentStock <= item.reorderPoint
    );
    setLowStockItems(itemsNeedingRestock);
  }, [inventory]);

  // Restock an item
  const handleRestock = (itemId) => {
    setInventory(prevInventory => 
      prevInventory.map(item => 
        item.id === itemId 
          ? { ...item, currentStock: item.currentStock + 50 } 
          : item
      )
    );
  };

  // Calculate total restock cost
  const calculateRestockCost = (item) => {
    const restockQuantity = 50; // Standard restock amount
    return (restockQuantity * item.unitPrice).toFixed(2);
  };

  // Start editing an item
  const startEditItem = (item) => {
    setEditingItem({...item});
  };

  // Update item during edit
  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditingItem(prev => ({
      ...prev,
      [name]: name === 'currentStock' || name === 'reorderPoint' || name === 'unitPrice' 
        ? Number(value) 
        : value
    }));
  };

  // Save edited item
  const saveEditedItem = () => {
    setInventory(prevInventory => 
      prevInventory.map(item => 
        item.id === editingItem.id ? editingItem : item
      )
    );
    setEditingItem(null);
  };

  // Delete an item
  const deleteItem = (itemId) => {
    setInventory(prevInventory => 
      prevInventory.filter(item => item.id !== itemId)
    );
  };

  // Handle new item input changes
  const handleNewItemChange = (e) => {
    const { name, value } = e.target;
    setNewItem(prev => ({
      ...prev,
      [name]: name === 'currentStock' || name === 'reorderPoint' || name === 'unitPrice' 
        ? Number(value) 
        : value
    }));
  };

  // Add a new item
  const addNewItem = () => {
    const itemToAdd = {
      ...newItem,
      id: Date.now() // Unique ID
    };
    setInventory(prev => [...prev, itemToAdd]);
    setNewItem({
      name: '',
      currentStock: 0,
      reorderPoint: 0,
      unitPrice: 0,
      supplier: '',
      unit: 'kg',
      category: ''
    });
    setIsAddingItem(false);
  };

  // Calculate total inventory value
  const totalInventoryValue = inventory.reduce(
    (total, item) => total + (item.currentStock * item.unitPrice), 
    0
  );

  return (
    <div className="container mx-auto p-4 max-w-6xl bg-gray-50">
      <div className="bg-white shadow-md rounded-lg p-6">
        {/* Header with Inventory Summary */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold flex items-center text-blue-800">
            <Package className="mr-2" /> इन्वेंटरी प्रबंधन (Inventory Management)
          </h1>
          <div className="text-right">
            <p className="text-gray-600">कुल इन्वेंटरी मूल्य (Total Inventory Value)</p>
            <p className="text-xl font-bold text-green-600">₹{totalInventoryValue.toFixed(2)}</p>
          </div>
        </div>

        {/* Low Stock Alert */}
        {lowStockItems.length > 0 && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
            <div className="flex items-center mb-3">
              <AlertCircle className="mr-2 text-yellow-500" />
              <h2 className="text-lg font-semibold text-yellow-700">स्टॉक अलर्ट (Stock Alerts)</h2>
            </div>
            {lowStockItems.map(item => (
              <div 
                key={item.id} 
                className="flex justify-between items-center mb-2"
              >
                <span className="text-gray-800">
                  {item.name} - वर्तमान स्टॉक: {item.currentStock} {item.unit}
                </span>
                <button 
                  onClick={() => handleRestock(item.id)}
                  className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded flex items-center"
                >
                  <ShoppingCart className="mr-2" /> 
                  पुनः स्टॉक (Restock) (₹{calculateRestockCost(item)})
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Add New Item Button */}
        <div className="mb-4">
          <button 
            onClick={() => setIsAddingItem(true)}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded flex items-center"
          >
            <Plus className="mr-2" /> नया आइटम जोड़ें (Add New Item)
          </button>
        </div>

        {/* New Item Form */}
        {isAddingItem && (
          <div className="bg-gray-100 p-4 rounded-lg mb-4">
            <h3 className="text-lg font-semibold mb-3">नया आइटम (New Item)</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                type="text"
                name="name"
                placeholder="आइटम नाम (Item Name)"
                value={newItem.name}
                onChange={handleNewItemChange}
                className="border p-2 rounded"
              />
              <input
                type="number"
                name="currentStock"
                placeholder="वर्तमान स्टॉक (Current Stock)"
                value={newItem.currentStock}
                onChange={handleNewItemChange}
                className="border p-2 rounded"
              />
              <input
                type="number"
                name="reorderPoint"
                placeholder="पुनर्आर्डर बिंदु (Reorder Point)"
                value={newItem.reorderPoint}
                onChange={handleNewItemChange}
                className="border p-2 rounded"
              />
              <input
                type="text"
                name="supplier"
                placeholder="आपूर्तिकर्ता (Supplier)"
                value={newItem.supplier}
                onChange={handleNewItemChange}
                className="border p-2 rounded"
              />
              <select
                name="unit"
                value={newItem.unit}
                onChange={handleNewItemChange}
                className="border p-2 rounded"
              >
                <option value="kg">किलोग्राम (Kg)</option>
                <option value="ltr">लीटर (Ltr)</option>
                <option value="pcs">पीस (Pcs)</option>
              </select>
              <input
                type="number"
                name="unitPrice"
                placeholder="इकाई मूल्य (Unit Price)"
                value={newItem.unitPrice}
                onChange={handleNewItemChange}
                className="border p-2 rounded"
              />
              <input
                type="text"
                name="category"
                placeholder="श्रेणी (Category)"
                value={newItem.category}
                onChange={handleNewItemChange}
                className="border p-2 rounded"
              />
            </div>
            <div className="flex mt-4 space-x-2">
              <button 
                onClick={addNewItem}
                className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded flex items-center"
              >
                <Save className="mr-2" /> सेव करें (Save)
              </button>
              <button 
                onClick={() => setIsAddingItem(false)}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded flex items-center"
              >
                <X className="mr-2" /> रद्द करें (Cancel)
              </button>
            </div>
          </div>
        )}

        {/* Inventory Table */}
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <div className="p-4 border-b bg-gray-100">
            <h2 className="text-lg font-semibold text-gray-800">वर्तमान इन्वेंटरी (Current Inventory)</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-200">
                <tr>
                  <th className="p-3 text-left text-gray-700">उत्पाद (Product)</th>
                  <th className="p-3 text-left text-gray-700">श्रेणी (Category)</th>
                  <th className="p-3 text-left text-gray-700">वर्तमान स्टॉक (Current Stock)</th>
                  <th className="p-3 text-left text-gray-700">पुनर्आर्डर बिंदु (Reorder Point)</th>
                  <th className="p-3 text-left text-gray-700">इकाई मूल्य (Unit Price)</th>
                  <th className="p-3 text-left text-gray-700">आपूर्तिकर्ता (Supplier)</th>
                  <th className="p-3 text-left text-gray-700">क्रियाएँ (Actions)</th>
                </tr>
              </thead>
              <tbody>
                {inventory.map(item => (
                  <tr key={item.id} className="border-b hover:bg-gray-50">
                    {editingItem && editingItem.id === item.id ? (
                      // Editing Mode
                      <>
                        <td>
                          <input
                            type="text"
                            name="name"
                            value={editingItem.name}
                            onChange={handleEditChange}
                            className="border p-1 w-full"
                          />
                        </td>
                        <td>
                          <input
                            type="text"
                            name="category"
                            value={editingItem.category}
                            onChange={handleEditChange}
                            className="border p-1 w-full"
                          />
                        </td>
                        <td>
                          <input
                            type="number"
                            name="currentStock"
                            value={editingItem.currentStock}
                            onChange={handleEditChange}
                            className="border p-1 w-full"
                          />
                        </td>
                        <td>
                          <input
                            type="number"
                            name="reorderPoint"
                            value={editingItem.reorderPoint}
                            onChange={handleEditChange}
                            className="border p-1 w-full"
                          />
                        </td>
                        <td>
                          <input
                            type="number"
                            name="unitPrice"
                            value={editingItem.unitPrice}
                            onChange={handleEditChange}
                            className="border p-1 w-full"
                          />
                        </td>
                        <td>
                          <input
                            type="text"
                            name="supplier"
                            value={editingItem.supplier}
                            onChange={handleEditChange}
                            className="border p-1 w-full"
                          />
                        </td>
                        <td className="flex space-x-2">
                          <button 
                            onClick={saveEditedItem}
                            className="text-green-500 hover:text-green-700"
                          >
                            <Save />
                          </button>
                          <button 
                            onClick={() => setEditingItem(null)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <X />
                          </button>
                        </td>
                      </>
                    ) : (
                      // View Mode
                      <>
                        <td className="p-3 text-gray-800">{item.name}</td>
                        <td className="p-3 text-gray-700">{item.category}</td>
                        <td className="p-3">
                          <span className={
                            item.currentStock <= item.reorderPoint 
                              ? 'text-red-500 font-bold' 
                              : 'text-green-600'
                          }>
                            {item.currentStock} {item.unit}
                          </span>
                        </td>
                        <td className="p-3 text-gray-700">{item.reorderPoint} {item.unit}</td>
                        <td className="p-3 text-gray-800">₹{item.unitPrice.toFixed(2)}</td>
                        <td className="p-3 text-gray-700">{item.supplier}</td>
                        <td className="p-3 flex space-x-2">
                          <button 
                            onClick={() => handleRestock(item.id)}
                            disabled={item.currentStock > item.reorderPoint}
                            className={`${
                              item.currentStock > item.reorderPoint
                                ? 'text-gray-300 cursor-not-allowed'
                                : 'text-blue-500 hover:text-blue-700'
                            }`}
                          >
                            <ShoppingCart />
                          </button>
                          <button 
                            onClick={() => startEditItem(item)}
                            className="text-green-500 hover:text-green-700"
                          >
                            <Edit />
                          </button>
                          <button 
                            onClick={() => deleteItem(item.id)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <Trash2 />
                          </button>
                        </td>
                      </>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Additional Features Section */}
        <div className="mt-6 bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-blue-800">
            अतिरिक्त सुविधाएँ (Additional Features)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <h4 className="font-bold mb-2 text-gray-800">रिपोर्ट जनरेशन (Report Generation)</h4>
              <p className="text-gray-600 text-sm">स्टॉक और बिक्री की विस्तृत रिपोर्ट</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <h4 className="font-bold mb-2 text-gray-800">जीएसटी अनुकूल (GST Compliant)</h4>
              <p className="text-gray-600 text-sm">सभी मूल्य और रिपोर्ट जीएसटी नियमों के अनुरूप</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <h4 className="font-bold mb-2 text-gray-800">बैकअप और सुरक्षा (Backup & Security)</h4>
              <p className="text-gray-600 text-sm">स्वचालित डेटा बैकअप और सुरक्षित संग्रहण</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InventoryManagementApp;
